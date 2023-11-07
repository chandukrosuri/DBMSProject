from flask import Flask, jsonify
import cx_Oracle

app = Flask(__name__)

# Set up DSN (Data Source Name)
# dsn = cx_Oracle.makedsn('HOST', 'PORT', sid='YOUR_SID')

# Establish the database connection
# connection = cx_Oracle.connect(user='USERNAME', password='PASSWORD', dsn=dsn)


@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
