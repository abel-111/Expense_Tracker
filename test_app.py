import pytest
import sqlite3
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client

def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200
def test_register_then_duplicate_fails(client):
    # first registration should succeed and redirect to /login
    response = client.post("/register", data={
        "username": "alice",
        "password": "pass123"
    })
    assert response.status_code == 302  # redirect means success

    # registering the same username again should fail, not redirect
    response = client.post("/register", data={
        "username": "alice",
        "password": "different"
    })
    assert response.status_code == 200  # re-renders register.html with an error
    assert b"already taken" in response.data
    # cleanup so this test can run again later
    conn = sqlite3.connect("expenses.db")
    conn.execute("DELETE FROM users WHERE username = 'alice'")
    conn.commit()
    conn.close()
def test_login_failure(client):
    # first register a user
    client.post("/register", data={"username": "bob", "password": "correct"})

    # try logging in with the wrong password
    response = client.post("/login", data={"username": "bob", "password": "wrong"})

    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

    # cleanup
    conn = sqlite3.connect("expenses.db")
    conn.execute("DELETE FROM users WHERE username = 'bob'")
    conn.commit()
    conn.close()
def test_idor_delete_protection(client):
    # register and login as user A
    client.post("/register", data={"username": "userA", "password": "passA"})
    client.post("/login", data={"username": "userA", "password": "passA"})

    # add an expense as user A
    client.post("/add", data={"category": "Food", "amount": "100", "date": "2024-01-01"})

    # get the expense ID
    conn = sqlite3.connect("expenses.db")
    row = conn.execute("SELECT id FROM expenses WHERE category = 'Food' AND amount = 100").fetchone()
    expense_id = row[0]
    conn.close()

    # logout and login as user B
    client.get("/logout")
    client.post("/register", data={"username": "userB", "password": "passB"})
    client.post("/login", data={"username": "userB", "password": "passB"})

    # user B tries to delete user A's expense
    client.post(f"/delete/{expense_id}")

    # expense should still exist
    conn = sqlite3.connect("expenses.db")
    row = conn.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    conn.close()

    assert row is not None  # delete was blocked

    # cleanup
    conn = sqlite3.connect("expenses.db")
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.execute("DELETE FROM users WHERE username IN ('userA', 'userB')")
    conn.commit()
    conn.close()
def test_idor_edit_protection(client):
    # register and login as user A
    client.post("/register", data={"username": "userA", "password": "passA"})
    client.post("/login", data={"username": "userA", "password": "passA"})

    # add an expense as user A
    client.post("/add", data={"category": "Food", "amount": "100", "date": "2024-01-01"})

    # get the expense ID
    conn = sqlite3.connect("expenses.db")
    row = conn.execute("SELECT id FROM expenses WHERE category = 'Food' AND amount = 100").fetchone()
    expense_id = row[0]
    conn.close()

    # logout and login as user B
    client.get("/logout")
    client.post("/register", data={"username": "userB", "password": "passB"})
    client.post("/login", data={"username": "userB", "password": "passB"})

    # user B tries to overwrite user A's expense
    client.post(f"/edit/{expense_id}", data={
        "category": "Hacked",
        "amount": "999",
        "date": "2024-06-01"
    })

    # user A's expense should be unchanged
    conn = sqlite3.connect("expenses.db")
    row = conn.execute("SELECT category, amount FROM expenses WHERE id = ?", (expense_id,)).fetchone()
    conn.close()

    assert row[0] == "Food"    # category unchanged
    assert row[1] == 100.0     # amount unchanged

    # cleanup
    conn = sqlite3.connect("expenses.db")
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.execute("DELETE FROM users WHERE username IN ('userA', 'userB')")
    conn.commit()
    conn.close()