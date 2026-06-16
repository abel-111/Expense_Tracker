import sqlite3
from flask import Flask,render_template,request,redirect,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from flask import session

app = Flask(__name__)
app.secret_key = "replace-this-with-something-random"  # needed for sessions to work
def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""create table if not exists users (
                id integer primary key autoincrement,
                username text unique,
                password text
        )""")    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            user_id INTEGER REFERENCES users(id),
            id INTEGER primary KEY AUTOINCREMENT,
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
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, amount, date FROM expenses WHERE user_id = ?", (session["user_id"],))
    expenses = cursor.fetchall()
    total = sum(expense[2] for expense in expenses)
    conn.close()
    return render_template("home.html", username=session["username"], expenses=expenses, total=total)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")
@app.route('/add',methods=['POST'])
def add_expense():
    category = request.form["category"]
    amount = request.form["amount"]
    date = request.form["date"]
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (user_id, category, amount, date) VALUES (?, ?, ?, ?)",(session["user_id"], category, amount, date))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", error="Username already taken")
        conn.close()
        return redirect(url_for("login"))

    return render_template("register.html")
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
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
if __name__ == '__main__':    app.run(debug=True)