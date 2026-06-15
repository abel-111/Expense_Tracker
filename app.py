import sqlite3
from flask import Flask,render_template,request,redirect,url_for
app = Flask(__name__)
def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            amount REAL,
            date TEXT DEFAULT (DATE('now'))
        )
    """)
    conn.commit()
    conn.close()

init_db()
@app.route("/")
def home():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, amount,date FROM expenses")
    expenses = cursor.fetchall()
    total = sum(expense[2] for expense in expenses)
    conn.close()
    return render_template("home.html", username="Abel", expenses=expenses, total=total)
@app.route('/add',methods=['POST'])
def add_expense():
    category = request.form["category"]
    amount = request.form["amount"]
    date = request.form["date"]
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (category, amount,date) VALUES (?, ?, ?)", (category, amount,date))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))
@app.route("/edit/<int:id>")
def edit_expense(id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, amount, date FROM expenses WHERE id = ?", (id,))
    expense = cursor.fetchone()
    conn.close()
    return render_template("edit.html", expense=expense)

@app.route("/edit/<int:id>", methods=["POST"])
def update_expense(id):
    category = request.form["category"]
    amount = request.form["amount"]
    date = request.form["date"]
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE expenses SET category = ?, amount = ?, date = ? WHERE id = ?", (category, amount, date, id))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))
@app.route("/delete/<int:id>")
def delete_expense(id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))
if __name__ == '__main__':    app.run(debug=True)