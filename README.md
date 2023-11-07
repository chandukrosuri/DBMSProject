# DBMS_Project

## Steps to run/develop the code in your local enviornment

 1. Clone the repo on your local machine and make sure you have Python 3.6 or above installed
 2. Create a virtual environment : `python -m venv dbms`
 3. Activate the virtual enviornment: `source dbms/bin/activate` for Linux/MacOS, and `.\dbms\Scripts\activate` for Windows
 4. Install all the required files: `pip install -r requirements.txt`
 5. Create a .env file in your main project directory and add the following information to it
    
	 `DB_HOST=your_host`  
	 `DB_SID=your_sid`  
	 `DB_USERNAME=your_username`  
	 `DB_PASSWORD=your_password`  
	 `SECRET_KEY=your_secret_key (A 256 bit random Encryption key)`  
	  
	Remember to replace the text with your information
 7. Run the Flask App `flask run`
