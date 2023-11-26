from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
import oracledb
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

app.secret_key = os.getenv('SECRET_KEY') # 256-bit encryption 

# # Set up DSN (Data Source Name)
# dsn = cx_Oracle.makedsn(os.getenv('DB_HOST'), os.getenv('DB_PORT'), sid=os.getenv('DB_SID'))

# Establish the database connection
connection = oracledb.connect(user=os.getenv('DB_USERNAME'), password=os.getenv('DB_PASSWORD'), dsn=os.getenv('DB_HOST') + '/' + os.getenv('DB_SID'))

# @app.route('/')
# def home():
#     return 'Welcome to DBMS Project'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Validation From SQL here
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        #Email Verification here

        flash('Registration successful, please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/', methods = ['GET'])
def userdahsboard():
    return render_template('userDashboard.html')

@app.route('/Q1', methods=['GET', 'POST'])
def process_q1():
    if request.method == 'POST':
        value1_q1 = int(request.form.get('value1_q1'))
        value2_q1 = int(request.form.get('value2_q1'))
        p1 = Person("John", 36)
        p2 = Person("John", 36)
        list1 = []
        list1.append(p1.to_dict())
        list1.append(p2.to_dict())

        # Perform some computation based on the form data
        result = value1_q1 + value2_q1  # Replace this with your actual computation

        # Return the result as JSON
        return {'result': list1}

    return render_template('Q1.html')

@app.route('/Q2', methods = ['GET','POST'])
def page2():
    if request.method=='POST':
        print(request.form.get('value1_q1'))
        print(request.form.get('value2_q1'))
    return render_template('Q2.html')

@app.route('/Q3', methods = ['GET','POST'])
def page3():
    if request.method=='POST':
        print(request.form.get('value1_q1'))
        print(request.form.get('value2_q1'))
    return render_template('Q3.html')

@app.route('/Q4', methods = ['GET','POST'])
def page4():
    if request.method=='POST':
        print(request.form.get('value1_q1'))
        print(request.form.get('value2_q1'))
    return render_template('Q4.html')

@app.route('/Q5', methods = ['GET','POST'])
def page5():
    if request.method=='POST':
        print(request.form.get('value1_q1'))
        print(request.form.get('value2_q1'))
    return render_template('Q5.html')

@app.route('/feedback', methods = ['GET', 'POST'])
def feedbackPage():
    if request.method == 'POST':
        feedback = request.form.get('feedback-text')
        rating = request.form.get('rating')
    return render_template('Q1.html', pageName = "feedback")

@app.route('/logout', methods = ['GET'])
def logout():
    return logout()
if __name__ == '__main__':
    app.run(debug=True)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def to_dict(self):
        return {'name': self.name, 'age': self.age}