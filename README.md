# Expense Tracker

A web application built with Python and Flask to track personal expenses.

## Current Features

- User registration with hashed passwords
- User login and logout with session management
- Each user sees only their own expenses
- Add expenses with category, amount, and date
- View all expenses in a list
- Edit existing expenses
- Delete expenses
- View total spending

## Technologies Used

- Python 3.14
- Flask 3.1.3
- SQLite (built-in Python library)
- Jinja2 (Flask templating)
- Werkzeug (password hashing)
- HTML

## Project Structure

expense-tracker/
├── app.py
├── expenses.db
└── templates/
    ├── home.html
    ├── login.html
    ├── register.html
    └── edit.html

## How to Run

1. Clone the repository
   git clone <your-repo-url>

2. Install Flask
   pip install flask

3. Run the app
   python app.py

4. Open browser and visit
   http://127.0.0.1:5000

## Status

In progress. Future features planned:
- Bootstrap styling
- Expense filtering
- Monthly totals
- CSV export