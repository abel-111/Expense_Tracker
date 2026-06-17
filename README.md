# Expense Tracker Web Application

A simple Expense Tracker web application built using Python, Flask, SQLite, and HTML. This project allows users to securely manage their personal expenses with authentication and full CRUD functionality.

---

## Features

### User Authentication
- User Registration
- User Login
- User Logout
- Password Hashing using Werkzeug
- Session Management using Flask Sessions

### Expense Management
- Add new expenses
- View all expenses
- Edit existing expenses
- Delete expenses
- Calculate total spending automatically

### Data Validation
- Validates amount input
- Prevents empty category and date fields
- Displays user-friendly error messages using Flask Flash Messages

### User-Specific Data
- Each user can only view and manage their own expenses
- Expenses are linked to registered user accounts

---

## Technologies Used

- Python 3
- Flask
- SQLite3
- HTML
- Jinja2 Templates
- Werkzeug Security

---

## Project Structure

```
expense-tracker/
│
├── app.py
├── expenses.db
│
└── templates/
    ├── home.html
    ├── login.html
    ├── register.html
    └── edit.html
```

---

## Database Design

### Users Table

| Column | Type |
|----------|----------|
| id | Integer (Primary Key) |
| username | Text (Unique) |
| password | Text (Hashed) |

### Expenses Table

| Column | Type |
|----------|----------|
| id | Integer (Primary Key) |
| user_id | Integer (Foreign Key) |
| category | Text |
| amount | Real |
| date | Text |

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/abel-111/expense-tracker.git
cd expense-tracker
```

### 2. Install Dependencies

```bash
pip install flask werkzeug
```

### 3. Run Application

```bash
python app.py
```

### 4. Open Browser

```
http://127.0.0.1:5000
```

---

## Screens Included

- Register Page
- Login Page
- Home Dashboard
- Add Expense Form
- Edit Expense Page
- Expense List with Total Spending

---

## Learning Outcomes

Through this project I learned:

- Flask Routing
- Flask Templates (Jinja2)
- Session Management
- User Authentication
- Password Hashing
- SQLite Database Operations
- CRUD Operations
- Form Handling
- Input Validation
- Database Relationships

---

## Future Improvements

- Bootstrap UI Design
- Expense Categories Chart
- Monthly Expense Summary
- Expense Search and Filter
- CSV Export
- User Profile Page
- Dark Mode

---

## Author

GitHub: https://github.com/abel-111