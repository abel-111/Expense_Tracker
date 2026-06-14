from flask import Flask,render_template,request,redirect,url_for
app = Flask(__name__)
expenses = []
@app.route('/')
def home():
    return render_template('home.html',username='Abel',expenses=expenses)
@app.route('/add',methods=['POST'])
def expense():
    category = request.form['category']
    amount = request.form['amount']
    expenses.append({'category': category, 'amount': amount})
    return redirect(url_for('home'))

if __name__ == '__main__':    app.run(debug=True)