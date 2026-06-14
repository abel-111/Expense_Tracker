from flask import Flask,render_template
app = Flask(__name__)
@app.route('/')
def home():
    expenses = [
        {"category": "Food", "amount": 250},
        {"category": "Travel", "amount": 100},
        {"category": "Shopping", "amount": 500},
    ]
    return render_template('home.html',username='Abel',expenses=expenses)
if __name__ == '__main__':    app.run(debug=True)