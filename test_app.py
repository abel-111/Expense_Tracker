import pytest
import sqlite3
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
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