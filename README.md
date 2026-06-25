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

### User Interface

- Responsive Bootstrap 5 design
- Shared base template using Jinja2 inheritance
- Navigation bar with authentication controls
- Bootstrap flash message alerts
- Dark mode toggle with ripple animation and localStorage persistence

### Expense Analytics

- Spending breakdown chart using Chart.js
- Category-wise expense visualization
- Automatic total expense calculation
- Delete confirmation prompt before removing an expense
- Monthly budget tracking with visual progress bar and overspend alerts
- Monthly expense reporting
- Monthly category-wise spending breakdown
- Doughnut chart visualization for monthly reports
---

## Technologies Used

- Python 3
- Flask
- SQLite3
- HTML5
- Bootstrap 5
- Chart.js
- Jinja2 Templates
- Werkzeug Security
- pytest (automated testing)
- python-dotenv (environment variable management)
- Gunicorn (production WSGI server)
---

## Project Structure

```
expense-tracker/
│
├── app.py
├── expenses.db
│
└── templates/
    ├── base.html
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
## Testing

Basic automated tests are included using `pytest`.

### Run tests
```bash
python -m pytest test_app.py -v
```

Current coverage:
- Login page loads correctly
- Duplicate username registration is rejected
- Login failure returns error message
- IDOR protection on delete (user cannot delete another user's expense)
- IDOR protection on edit (user cannot overwrite another user's expense)

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/abel-111/expense-tracker.git
cd expense-tracker
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the project root with a secret key:

```bash
SECRET_KEY=your_random_secret_key_here
```

You can generate one with:

```bash
python -c "import secrets; print(secrets.token_hex(24))"
```

### 4. Run Application

```bash
python app.py
```

### 5. Open Browser

```
http://127.0.0.1:5000
```

---
## Live Demo

🔗 [View live app](https://expense-tracker-p6bl.onrender.com/) *(hosted on Render free tier — first load may take 20–30 seconds if the app has been idle)*

---

## Screens Included

- Register Page
- Login Page
- Home Dashboard
- Add Expense Form
- Edit Expense Page
- Expense List with Total Spending
- Settings Page
- Monthly Report Page
- Category Breakdown Chart

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
- Flask Flash Messages
- CSRF Protection
- Environment Variables using python-dotenv
- Chart.js Integration
- Monthly Expense Reporting

---

## Future Improvements

- Expense search and filtering
- CSV export functionality
- User profile management
- Expanded automated test coverage (login failure, IDOR protection, edit/delete ownership checks)
- Persistent database (PostgreSQL) so data survives free-tier restarts

---

## Author

GitHub: https://github.com/abel-111