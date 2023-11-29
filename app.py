from flask import Flask, render_template, request, redirect, url_for, flash, session, g, jsonify, json
from sql import assign_sql_query
import os
import oracledb
from dotenv import load_dotenv
import hashlib
import ast

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
    # print(get_max_value("education_gdp_ratio",2000))
    db = get_db()
    cursor = db.cursor()
    query = f"select COUNT(DISTINCT table_name) from user_tab_privs where not table_name = 'BIN$Cl76UdyDWzrgY1Ji8gq87Q==$0' and not table_name = 'USERS' and not table_name = 'SUNEETJAIN' and not table_name = 'KROSURIS'"
    cursor.execute(query)
    result = cursor.fetchone()
    number_of_tables = result[0]
    query = f"select DISTINCT table_name from user_tab_privs where not table_name = 'BIN$Cl76UdyDWzrgY1Ji8gq87Q==$0' and not table_name = 'USERS' and not table_name = 'SUNEETJAIN' and not table_name = 'KROSURIS'"
    cursor.execute(query)
    result = cursor.fetchall()
    sum = 0
    # print(result)
    for row in result:
        table_name = row[0]
        query = f"select count(*) from rvarki.{table_name}"
        print(query)
        cursor.execute(query)
        res = cursor.fetchone()
        sum += res[0]
    sum = '{:,}'.format(sum)
    number_of_tuples = sum
    return render_template('home.html',number_of_tuples=number_of_tuples,number_of_tables=number_of_tables)


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

@app.route('/api/max_value')
def max_value():
    year = request.args.get('year')
    print("year: "+year)
    query_type = request.args.get('queryType')
    print("qt: "+query_type)
    
    max_value = get_max_value(query_type,int(year))  # Your function to calculate the max value
    return jsonify({'max_value': max_value})

@app.route('/api/data')
def heat_data():
    query_type = request.args.get('queryType')
    year = request.args.get('year')
    data = get_map_data(query_type,int(year))
    # print(data)
    return jsonify(data)


def assign_table_names(query_type):
    if query_type == "education_gdp_ratio":
        return ['rvarki.average_schooling_years','rvarki.gdp']
    elif  query_type == "debt_expen_ratio":
        return ['rvarki.government_debt', 'rvarki.government_expenditure']
    elif query_type == "debt_expen_ratio":
        return ['rvarki.GOVERNMENT_DEBT','rvarki.GOVERNMENT_EXPENDITURE']
    elif query_type == "medical_contribution":
        return ["rvarki.NUMBER_OF_MEDICALDOCTORS","rvarki.NUMBER_OF_DENTISTS"]
    elif query_type == "obesity_change":
        return ["rvarki.obesity","rvarki.continent"]
    elif query_type == "suicide_mean":
        return ["rvarki.suicide_rate",None]
    elif query_type == "happiness_change":
        return ["rvarki.happiness","rvarki.continent"]
    elif query_type == "pollution_rank":
        return ["RVARKI.DEATHS_DUETO_AIRPOLLUTION",None]
    
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

@app.route('/years/<query_type>', methods = ['GET'])
def get_years_by_query_type(query_type):
    table1,table2 = assign_table_names(query_type)
    years = get_years(table1, table2)
    return jsonify({'years': list(sorted(years))})

def get_years(table1, table2):
    db = get_db()
    cursor = db.cursor()
    query_1 = f"select DISTINCT t1.year from {table1} t1"
    query_2 = f"select DISTINCT t2.year from {table2} t2"
    cursor.execute(query_1)
    table_1_years = cursor.fetchall()
    cursor.execute(query_2)
    table_2_years = cursor.fetchall()
    cursor.close()

    all_years = [year for (year,) in table_1_years + table_2_years]
    minyear = min(all_years)
    maxyear = max(all_years)

    return set(range(minyear, maxyear + 1))

def get_year(table):
    db = get_db()
    cursor = db.cursor()
    query = f"select DISTINCT t.year from {table} t"
    cursor.execute(query)
    years = cursor.fetchall()
    cursor.close()
    all_years = [year for (year,) in years]
    minyear = min(all_years)
    maxyear = max(all_years)
    return set(range(minyear, maxyear + 1))

@app.route("/query-data", methods = ['POST'])
def get_data():
    print(request.form)
    value1_q1 = int(request.form.get('value1_q1'))
    value2_q1 = int(request.form.get('value2_q1'))
    country = ast.literal_eval(request.form.getlist('value3_q1')[0])
    print(country)
    query_type = request.form.get('query_type')
    # print("qt: "+query_type)
    # print("bool: "+str(query_type == "education_gdp_ratio"))
    
    db = get_db()
    cursor = db.cursor()
    if query_type == "education_gdp_ratio":
        num_countries = len(country)
        query = assign_sql_query(query_type, num_countries)
        # print(query)
        bind_variables = {'start_year': value1_q1, 'end_year': value2_q1}
        for i, country in enumerate(country, start=1):
            bind_variables[f'country{i}'] = country

        cursor.execute(query, bind_variables)
        result = cursor.fetchall()
        cursor.close()
        print(result)
    # Process the results to calculate the GDP/Education ratio
        final_data = [{
            'year': row[0],
            'country': row[1],
            'ratio': (row[2] / row[3]) if row[3] else None  # Ensure not to divide by zero
        } for row in result]
        return jsonify(final_data)
    
    elif query_type == "debt_expen_ratio":
        num_countries = len(country)
        print("num_coun:" + str(num_countries))
        query = assign_sql_query(query_type, num_countries)
        # print(query)
        bind_variables = {'start_year': value1_q1, 'end_year': value2_q1}
        for i, country in enumerate(country, start=1):
            bind_variables[f'country{i}'] = country
        print(bind_variables)
        cursor.execute(query, bind_variables)
        result = cursor.fetchall()
        cursor.close()
        print(result)
        final_data = [{
            'year': row[0],
            'country': row[1],
            'ratio': (row[2] / row[3]) if row[3] else None  # Ensure not to divide by zero
        } for row in result]
        return jsonify(final_data)
    
    elif query_type == "happiness_change":
        num_countries = len(country)
        query = assign_sql_query(query_type, num_countries)
        print(query)
        bind_variables = {'start_year': value1_q1, 'end_year': value2_q1}
        for i, country in enumerate(country, start=1):
            bind_variables[f'country{i}'] = country
        cursor.execute(query, bind_variables)
        result = cursor.fetchall()
        cursor.close()
        print(result)
        final_data = [{
            'country': row[0],
            'year': row[1],
            'ratio': row[4],  # Ensure not to divide by zero
        } for row in result]
        # print(final_data)
        return jsonify(final_data)
    
    elif query_type == "obesity_change":
        num_countries = len(country)
        query = assign_sql_query(query_type, num_countries)
        print(query)
        bind_variables = {'start_year': value1_q1, 'end_year': value2_q1}
        for i, country in enumerate(country, start=1):
            bind_variables[f'country{i}'] = country
        cursor.execute(query,bind_variables)
        result = cursor.fetchall()
        cursor.close()
        print(result)
        final_data = [{
            'country': row[0],
            'year': row[1],
            'ratio': row[4],  # Ensure not to divide by zero
        } for row in result]
        print(final_data)
        return jsonify(final_data)
    
    elif query_type == "suicide_mean":
        num_countries = len(country)
        query = assign_sql_query(query_type, num_countries)
        print(query)
        bind_variables = {'start_year': value1_q1, 'end_year': value2_q1}
        for i, country in enumerate(country, start=1):
            bind_variables[f'country{i}'] = country
        cursor.execute(query,bind_variables)
        result = cursor.fetchall()
        cursor.close()
        print(result)
        final_data = [{
            'country': row[2],
            'year': row[0],
            'ratio': row[1],  # Ensure not to divide by zero
        } for row in result]
        print(final_data)
        return jsonify(final_data)
    
    elif query_type == "pollution_rank":
        num_countries = len(country)
        query = assign_sql_query(query_type, num_countries)
        print(query)
        bind_variables = {'start_year': value1_q1, 'end_year': value2_q1}
        for i, country in enumerate(country, start=1):
            bind_variables[f'country{i}'] = country
        cursor.execute(query,bind_variables)
        result = cursor.fetchall()
        cursor.close()
        print(result)
        final_data = [{
            'year': row[0],
            'country': row[1],
            'ratio': row[3],  # Ensure not to divide by zero
        } for row in result]
        return jsonify(final_data)
    
    elif query_type == "medical_contribution":
        num_countries = len(country)
        query = assign_sql_query(query_type, num_countries)
        print(query)
        bind_variables = {'start_year': value1_q1, 'end_year': value2_q1}
        for i, country in enumerate(country, start=1):
            bind_variables[f'country{i}'] = country
        cursor.execute(query,bind_variables)
        result = cursor.fetchall()
        cursor.close()
        # print(result)
        final_data = [{
            'country': row[1],
            'year': row[0],
            'ratio': row[4],  # Ensure not to divide by zero
        } for row in result]
        print(final_data)
        return jsonify(final_data)

@app.route('/dashboard', methods = ['GET'])
def userdahsboard():
    return render_template('userDashboard.html')

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
    return render_template('feedback.html', pageName = "feedback")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Remove 'logged_in' from session
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


def get_common_attributes(arr1,arr2):
        return set(arr1).intersection(set(arr2))
    

@app.route('/query-page/<page_number>', methods=['GET', 'POST'])
def query_page(page_number):
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    print("page-number: "+page_number)
    htmlPage = page_number
    if request.method == 'POST':
        # Process the selected query and parameters
        query_type = request.get_data(as_text=True)
        # Additional parameters based on the selected query
        if query_type == "education_gdp_ratio":
            print("entered: " + query_type)
            country_education = get_available_countries('rvarki.average_schooling_years')
            country_gpd = get_available_countries('rvarki.gdp')
            final_country = get_common_attributes(country_education,country_gpd)
            years = get_years('rvarki.average_schooling_years', 'rvarki.gdp')
            htmlPage = 1
            return jsonify({'final_country': list(sorted(final_country)) , 'table_name': query_type, 'years': list(sorted(years))})      

        elif query_type == "debt_expen_ratio":
            table1,table2 = assign_table_names(query_type)
            country_debt = get_available_countries(table1)
            country_expen = get_available_countries(table2)
            final_country = get_common_attributes(country_debt,country_expen)
            years = get_years(table1, table2)
            htmlPage = 1
            return jsonify({'final_country': list(sorted(final_country)) , 'table_name': query_type, 'years': list(sorted(years))})
        
        elif query_type == "happiness_change":
            htmlPage = 2
            query = """
                WITH yearly_avg AS (
                    SELECT c.continent, h.year, AVG(h.cantril_ladder_score) AS avg_happiness
                    FROM rvarki.happiness h
                    INNER JOIN rvarki.continent c ON h.countryname = c.country
                    GROUP BY c.continent, h.year
                ),
                yearly_avg_lag AS (
                    SELECT continent, year, avg_happiness, LAG(avg_happiness, 1) OVER (PARTITION BY continent ORDER BY year) AS prev_year_happiness
                    FROM yearly_avg
                )
                SELECT DISTINCT continent
                FROM yearly_avg_lag
                WHERE prev_year_happiness IS NOT NULL
                ORDER BY continent
                """
            db = get_db()
            cursor = db.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            years = get_year('rvarki.happiness')
            cursor.close()
            final_data = [{'continent': row[0]} for row in result]
            return jsonify({"final_country": list({i['continent'] for i in final_data}) , 'table_name': query_type, 'years': list(sorted(years))})
        
        elif query_type == "obesity_change":
            htmlPage = 2
            query = """
                WITH yearly_avg_obesity AS (
                    SELECT c.continent, o.year, AVG(o.bothsexes) AS avg_obesity
                    FROM rvarki.obesity o
                    INNER JOIN rvarki.continent c ON o.countryname = c.country
                    GROUP BY c.continent, o.year
                ),
                yearly_avg_obesity_lag AS (
                    SELECT continent, year, avg_obesity, LAG(avg_obesity, 1) OVER (PARTITION BY continent ORDER BY year) AS prev_year_obesity
                    FROM yearly_avg_obesity
                )
                SELECT DISTINCT continent
                FROM yearly_avg_obesity_lag
                WHERE prev_year_obesity IS NOT NULL
                ORDER BY continent
                """
            db = get_db()
            cursor = db.cursor()
            print("Generated SQL query:", query)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            years = get_year('rvarki.obesity')
            final_data = [{'continent': row[0]} for row in result]
            return jsonify({"final_country": list({i['continent'] for i in final_data}) , 'table_name': query_type, 'years': list(sorted(years))})
        
        elif query_type == "suicide_mean":
            htmlPage = 3
            final_country = get_available_countries("rvarki.suicide_rate")
            years = get_year('rvarki.suicide_rate')
            return jsonify({'final_country': list(sorted(final_country)) , 'table_name': query_type, 'years': list(sorted(years))})  
        
        elif query_type == "pollution_rank":
            htmlPage = 4
            final_country = get_available_countries("RVARKI.DEATHS_DUETO_AIRPOLLUTION")
            years = get_year('RVARKI.DEATHS_DUETO_AIRPOLLUTION')
            return jsonify({'final_country': list(sorted(final_country)) , 'table_name': query_type, 'years': list(sorted(years))})
        
        elif query_type == "medical_contribution":
            htmlPage = 5
            table1,table2 = assign_table_names(query_type)
            country_doctors = get_available_countries(table1)
            country_dentists = get_available_countries(table2)
            final_country = get_common_attributes(country_doctors,country_dentists)
            years = get_years(table1, table2)
            return jsonify({'final_country': list(sorted(final_country)) , 'table_name': query_type, 'years': list(sorted(years))})
        # Call a function to handle the query and generate results (e.g., data for the graph)
        # query_results = handle_query(query_type, **params)
        # return jsonify(query_results)

    return render_template('Q'+ str(htmlPage) +'.html')

def get_map_data(query_type,year):
    if query_type == "education_gdp_ratio":
        query = """
        SELECT rvarki.gdp.year, rvarki.gdp.countryname, ROUND((rvarki.gdp.gdp/rvarki.average_schooling_years.avg_yearsof_schooling),2) as ratio
        FROM rvarki.gdp 
        JOIN rvarki.average_schooling_years 
        ON rvarki.gdp.countryname = rvarki.average_schooling_years.countryname 
        AND rvarki.gdp.year = rvarki.average_schooling_years.year 
        WHERE rvarki.gdp.year = :year
        ORDER BY countryname
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute(query,{'year':year})
        result = cursor.fetchall()
        final_data = [{
            'country': row[1],
            'ratio': row[2]  # Ensure not to divide by zero
        } for row in result]
        return final_data

def get_max_value(query_type,year):
    if query_type == "education_gdp_ratio":
        print(1)
        query = """
        SELECT MAX(ROUND((rvarki.gdp.gdp/rvarki.average_schooling_years.avg_yearsof_schooling),2)) as ratio
                FROM rvarki.gdp 
                JOIN rvarki.average_schooling_years 
                ON rvarki.gdp.countryname = rvarki.average_schooling_years.countryname 
                AND rvarki.gdp.year = rvarki.average_schooling_years.year 
                WHERE rvarki.gdp.year = :year
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute(query,{'year':year})
        result = cursor.fetchone()
        print(result[0])
        return result[0]


if __name__ == '__main__':
    app.run(debug=True)

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def to_dict(self):
        return {'name': self.name, 'age': self.age}
