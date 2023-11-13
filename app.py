from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import os
import oracledb
from dotenv import load_dotenv
import hashlib

app = Flask(__name__)

load_dotenv()

app.secret_key = os.getenv('SECRET_KEY') # 256-bit encryption 

# Establish the database connection
def get_db():
    if 'db' not in g:
        g.db = oracledb.connect(user=os.getenv('DB_USERNAME'), password=os.getenv('DB_PASSWORD'), dsn=os.getenv('DB_HOST') + "/" + os.getenv('DB_SID'))
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def home():
    return 'Welcome to DBMS Project'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        pass_hash = hashlib.sha256(password.encode('UTF-8')).hexdigest()
        # Validation From SQL here

        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute("SELECT * FROM suneetjain.users WHERE email= :email",[email])
            ret = cursor.fetchall()
            # print(ret)
            if ret == []:
                flash("This account doesn't exist! Check credentials and try again.",'danger')
                return redirect(url_for('login'))
            else:
                if ret[0][3] != pass_hash:
                    flash("Invalid credentials",'danger')
                    return redirect(url_for('login'))

        except oracledb.DatabaseError as e:
            error, = e.args
            return e
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        pass_hash = hashlib.sha256(password.encode('UTF-8')).hexdigest()

        #Email Verification here
        db = get_db()
        cursor = db.cursor()

        try:
            cursor.execute("INSERT INTO suneetjain.users (name, email, password_hash) VALUES (:name, :email, :password_hash)", [name, email, pass_hash])
            db.commit()  # Commit changes
            # return "User registered successfully!"
        except oracledb.DatabaseError as e:
            db.rollback()  # Rollback changes
            error, = e.args
            # print(e)
            if error.code == 1:
                flash('Account already exists!','danger')
            else:
                return f"An error occurred: {e}"
        else:
            cursor.close()
            flash('Registration successful, please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
