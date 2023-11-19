# Import libraries
import sys
import csv
import os

data = "../data/births_attended.csv"
sql = "../sql_commands/births_attended.sql"
country_sql = "../sql_commands/births_attended_country.sql"
year_sql = "../sql_commands/births_attended_year.sql"

TABLE_NAME = "BIRTHS_ATTENDEDBY_SKILLED_HEALTHPROFESSIONAL"

# Create .sql file for births attended
with open(data, 'r') as infile:
    with open(sql, 'w') as outfile:
         with open(country_sql, 'w') as countryfile:
            with open(year_sql, 'w') as yearfile:
                csv_reader = csv.reader(infile)
                # Skip the first two header rows
                next(csv_reader)
                hiID = 0
                for row in csv_reader:
                    COUNTRY = row[0].split("(")[0].replace("'","")
                    YEARS = row[1].split("-")
                    BIRTHS = row[2] if len(row[2]) != 0 else "NULL"
                    for YEAR in YEARS:
                        outfile.write("INSERT INTO " + TABLE_NAME + " VALUES (" + str(hiID) + "," + "'" + COUNTRY + "'" + "," + YEAR + "," + BIRTHS + ");" + "\n")
                        countryfile.write("INSERT INTO " + "COUNTRY" + " VALUES (" + "'" + COUNTRY + "'" + ");" + "\n")
                        yearfile.write("INSERT INTO " + "TIME_YEAR" + " VALUES (" + YEAR + ");" + "\n")
                        hiID += 1 
           