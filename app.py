from flask import Flask, render_template, request, redirect, url_for, flash, session, g, jsonify
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
    # print(len(final_country),final_country)
    print(get_data())
    # print(get_years())
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

def get_common_attributes(arr1,arr2):
        return set(arr1).intersection(set(arr2))

def assign_table_names(query_type):
    if query_type == "education_gdp_ratio":
        return ['rvarki.average_schooling_years','rvarki.gdp']
    elif query_type == "debt_expen_ratio":
        return ['rvarki.GOVERNMENT_DEBT','rvarki.GOVERNMENT_EXPENDITURE']
    
def get_available_countries(table_name):
    db = get_db()
    cursor = db.cursor()
    query = f"select DISTINCT countryname from {table_name} order by countryname"
    cursor.execute(query)
    countries = cursor.fetchall()
    cursor.close()
    arr = []
    for _ in countries:
        arr.append(_[0])
    return arr  # Returns an array with names of countries in alphabetical order

@app.route('/query_page', methods=['GET', 'POST'])
def query_page():
    if request.method == 'POST':
        # Process the selected query and parameters
        query_type = request.form.get('query_type')
        # Additional parameters based on the selected query
        if query_type == "education_gdp_ratio":
            country_education = get_available_countries('rvarki.average_schooling_years')
            country_gpd = get_available_countries('rvarki.gdp')
            final_country = get_common_attributes(country_education,country_gpd)
            return jsonify({'final_country': final_country , 'table_name': query_type})      

        elif query_type == "debt_expen_ratio":
            table1,table2 = assign_table_names(query_type)
            country_debt = get_available_countries(table1)
            country_expen = get_available_countries(table2)
            final_country = get_common_attributes(country_debt,country_expen)
            return jsonify({'final_country': final_country , 'table_name': query_type})   



        # Call a function to handle the query and generate results (e.g., data for the graph)
        # query_results = handle_query(query_type, **params)
        # return jsonify(query_results)

    return render_template('query_page.html')
    
def assign_sql_query(query_type):
    if query_type == "education_gdp_ratio":
        # query = f"select rvarki.gdp.year,rvarki.gdp.gdp,rvarki.average_schooling_years.avg_yearsof_schooling from rvarki.gdp join rvarki.average_schooling_years on rvarki.gdp.countryname=rvarki.average_schooling_years.countryname and rvarki.gdp.year=rvarki.average_schooling_years.year where rvarki.gdp.countryname = {country} order by year;"
        query = """
        SELECT rvarki.gdp.year, rvarki.gdp.gdp, rvarki.average_schooling_years.avg_yearsof_schooling 
        FROM rvarki.gdp 
        JOIN rvarki.average_schooling_years 
        ON rvarki.gdp.countryname = rvarki.average_schooling_years.countryname 
        AND rvarki.gdp.year = rvarki.average_schooling_years.year 
        WHERE rvarki.gdp.countryname = :country 
        ORDER BY year
        """
        return query
    elif query_type == "debt_expen_ratio":
        query = """
        SELECT rvarki.government_debt.year, rvarki.government_debt.governmentdebt, rvarki.GOVERNMENT_EXPENDITURE.GOVERNMENT_EXPENDITURE 
        FROM rvarki.GOVERNMENT_DEBT
        JOIN rvarki.GOVERNMENT_EXPENDITURE 
        ON rvarki.GOVERNMENT_DEBT.countryname = rvarki.GOVERNMENT_EXPENDITURE.countryname 
        AND rvarki.GOVERNMENT_DEBT.year = rvarki.GOVERNMENT_EXPENDITURE.year 
        WHERE rvarki.GOVERNMENT_DEBT.countryname = :country
        ORDER BY year
        """
        return query

def get_years():
    db = get_db()
    cursor = db.cursor()
    # query_type = request.args.get('query_type')
    # country = request.args.get('country')
    query_type = "debt_expen_ratio"
    country = "India"
    # table1,table2 = assign_table_names(query_type)
    # subq = assign_sql_query(query_type)
    # print(subq)
    query = assign_sql_query(query_type)
    print(query)
    cursor.execute(query, {'country': country})
    result = cursor.fetchall()
    cursor.close()
    if result:
        years = [row[0] for row in result]
        print(years)
        return jsonify({'years_range': (min(years), max(years))})
    else:
        return jsonify({'error': 'No data found for the selected country'})

def get_data():
    db = get_db()
    cursor = db.cursor()
    query_type = "debt_expen_ratio"
    country = "India"
    # query_type = request.args.get('query_type')
    # country = request.args.get('country')
    if query_type == "education_gdp_ratio":
        query = assign_sql_query(query_type)
        print(query)
        cursor.execute(query,{'country': country})
        result = cursor.fetchall()
        cursor.close()

    # Process the results to calculate the GDP/Education ratio
        final_data = [{
            'year': row[0],
            'ratio': (row[1] / row[2]) if row[2] else None  # Ensure not to divide by zero
        } for row in result]
        print(final_data)
        return jsonify(final_data)
    
    elif query_type == "debt_expen_ratio":
        query = assign_sql_query(query_type)
        print(query)
        cursor.execute(query,{'country': country})
        result = cursor.fetchall()
        cursor.close()
        print(result)
    # Process the results to calculate the Debt/Expen ratio
        # for row in result:
        #     print(row[0],row[1],row[2])
        final_data = [{
            'year': row[0],
            'ratio': (row[1] / row[2]) if row[1] and row[2] else None  # Ensure not to divide by zero
        } for row in result]
        print(final_data)
        return jsonify(final_data)




if __name__ == '__main__':
    app.run(debug=True)
