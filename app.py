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
            amount REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()
@app.route('/')
@app.route("/")
def home():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, amount FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    return render_template("home.html", username="Abel", expenses=expenses)
@app.route('/add',methods=['POST'])
@app.route("/add", methods=["POST"])
def add_expense():
    category = request.form["category"]
    amount = request.form["amount"]
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (category, amount) VALUES (?, ?)", (category, amount))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))
if __name__ == '__main__':    app.run(debug=True)