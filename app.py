import sqlite3
import os
from dotenv import load_dotenv
from flask import Flask,render_template,request,redirect,url_for, session, flash
from werkzeug.security import generate_password_hash,check_password_hash
from flask_wtf import CSRFProtect
from flask import session
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("SECRET_KEY is not set. Did you create a .env file?")
csrf = CSRFProtect(app)
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
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN budget REAL DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE expenses ADD COLUMN notes TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()

init_db()
@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, category, amount, date, notes FROM expenses WHERE user_id = ? ORDER BY date DESC, id DESC",
        (session["user_id"],)
    )
    expenses = cursor.fetchall()
    total = sum(expense[2] for expense in expenses)

    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY category",
        (session["user_id"],)
    )
    category_totals = cursor.fetchall()
    
    cursor.execute(
        """SELECT SUM(amount) FROM expenses
        WHERE user_id = ? AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')""",
        (session["user_id"],)
    )
    monthly_row = cursor.fetchone()
    monthly_total = monthly_row[0] if monthly_row[0] else 0

    cursor.execute("SELECT budget FROM users WHERE id = ?", (session["user_id"],))
    budget_row = cursor.fetchone()
    budget = budget_row[0] if budget_row and budget_row[0] else 0
    conn.close()
    chart_labels = [row[0] for row in category_totals]
    chart_values = [row[1] for row in category_totals]

    return render_template(
    "home.html",
    username=session["username"],
    expenses=expenses,
    total=total,
    chart_labels=chart_labels,
    chart_values=chart_values,
    monthly_total=monthly_total,
    budget=budget
    )
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or not password:
            return render_template("login.html", error="Username and password are required.")

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
@app.route('/add', methods=['POST'])
def add_expense():
    if "user_id" not in session:
        return redirect(url_for("login"))

    category = request.form["category"]
    amount = request.form["amount"]
    date = request.form["date"]
    notes = request.form.get("notes", "")

    try:
        amount = float(amount)
    except ValueError:
        flash("Amount must be a valid number.")
        return redirect(url_for("home"))

    if not category or not date:
        flash("Category and date are required.")
        return redirect(url_for("home"))

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (user_id, category, amount, date, notes) VALUES (?, ?, ?, ?, ?)", (session["user_id"], category, amount, date, notes))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or not password:
            return render_template("register.html", error="Username and password are required.")

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
            flash("Account created! Please log in.", "success")
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", error="Username already taken")
        conn.close()
        return redirect(url_for("login"))

    return render_template("register.html")
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_expense(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    if request.method == "POST":
        category = request.form["category"]
        amount = request.form["amount"]
        date = request.form["date"]
        notes = request.form.get("notes", "")

        try:
            amount = float(amount)
        except ValueError:
            conn.close()
            flash("Amount must be a valid number.")
            return redirect(url_for("home"))

        if not category or not date:
            conn.close()
            flash("Category and date are required.")
            return redirect(url_for("home"))

        cursor.execute(
            "UPDATE expenses SET category = ?, amount = ?, date = ?, notes = ? WHERE id = ? AND user_id = ?",
            (category, amount, date, notes, id, session["user_id"])
        )
        conn.commit()
        conn.close()
        return redirect(url_for("home"))

    # GET — fetch the expense and show the form
    cursor.execute(
        "SELECT id, category, amount, date, notes FROM expenses WHERE id = ? AND user_id = ?",
        (id, session["user_id"])
    )
    expense = cursor.fetchone()
    conn.close()
    if expense is None:
        return redirect(url_for("home"))
    return render_template("edit.html", expense=expense)
@app.route("/delete/<int:id>", methods=["POST"])
def delete_expense(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ? AND user_id = ?", (id, session["user_id"]))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
@app.route("/settings", methods=["GET", "POST"])
def settings():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    if request.method == "POST":
        budget = request.form["budget"]
        try:
            budget = float(budget)
            if budget < 0:
                raise ValueError
        except ValueError:
            conn.close()
            flash("Please enter a valid budget amount.", "danger")
            return redirect(url_for("settings"))

        cursor.execute(
            "UPDATE users SET budget = ? WHERE id = ?",
            (budget, session["user_id"])
        )
        conn.commit()
        conn.close()
        flash("Budget updated successfully.", "success")
        return redirect(url_for("home"))

    cursor.execute("SELECT budget FROM users WHERE id = ?", (session["user_id"],))
    row = cursor.fetchone()
    conn.close()
    current_budget = row[0] if row and row[0] else 0
    return render_template("settings.html", current_budget=current_budget)
@app.route("/report")
def report():
    if "user_id" not in session:
        return redirect(url_for("login"))

    from datetime import date
    selected_month = request.args.get("month", date.today().strftime("%Y-%m"))

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT id, category, amount, date, notes FROM expenses
           WHERE user_id = ? AND strftime('%Y-%m', date) = ?
           ORDER BY date DESC, id DESC""",
        (session["user_id"], selected_month)
    )
    
    expenses = cursor.fetchall()

    cursor.execute(
        """SELECT category, SUM(amount) FROM expenses
           WHERE user_id = ? AND strftime('%Y-%m', date) = ?
           GROUP BY category ORDER BY SUM(amount) DESC""",
        (session["user_id"], selected_month)
    )
    category_totals = cursor.fetchall()
    conn.close()

    monthly_total = sum(e[2] for e in expenses)

    return render_template(
        "report.html",
        selected_month=selected_month,
        expenses=expenses,
        category_totals=category_totals,
        monthly_total=monthly_total
    )
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)