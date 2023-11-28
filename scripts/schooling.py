# Import libraries
import sys
import csv
import os

data = "../data/mean-years-of-schooling-long-run.csv"
sql = "../sql_commands/schooling.sql"
country_sql = "../sql_commands/schooling_country.sql"
year_sql = "../sql_commands/schooling_year.sql"

TABLE_NAME = "AVERAGE_SCHOOLING_YEARS"

# Create .sql file for average schooling
with open(data, 'r') as infile:
    with open(sql, 'w') as outfile:
        with open(country_sql, 'w') as countryfile:
            with open(year_sql, 'w') as yearfile:
                csv_reader = csv.reader(infile)
                # Skip the first two header rows
                next(csv_reader)
                hiID = 0
                for row in csv_reader:
                    row = row[0].split(";")
                    COUNTRY = row[0].split("(")[0].replace("'","")
                    YEAR = row[2]
                    SCHOOLING = row[3] if len(row[3]) != 0 else "NULL"
                    outfile.write("INSERT INTO " + TABLE_NAME + " VALUES (" + str(hiID) + "," + "'" + COUNTRY + "'" + "," + YEAR + "," + SCHOOLING + ");" + "\n")
                    countryfile.write("INSERT INTO " + "COUNTRY" + " VALUES (" + "'" + COUNTRY + "'" + ");" + "\n")
                    yearfile.write("INSERT INTO " + "TIME_YEAR" + " VALUES (" + YEAR + ");" + "\n")
                    hiID += 1