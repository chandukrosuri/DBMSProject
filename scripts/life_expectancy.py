# Import libraries
import sys
import csv
import os

data = "../data/life_expectancy.csv"
sql = "../sql_commands/life_expectancy.sql"
country_sql = "../sql_commands/life_expectancy_country.sql"
year_sql = "../sql_commands/life_expectancy_year.sql"

TABLE_NAME = "LIFE_EXPECTANCY"

# Create .sql file for life expectancy
with open(data, 'r') as infile:
    with open(sql, 'w') as outfile:
         with open(country_sql, 'w') as countryfile:
            with open(year_sql, 'w') as yearfile:
                csv_reader = csv.reader(infile)
                # Skip the first two header rows
                next(csv_reader)
                next(csv_reader)
                hiID = 0
                for row in csv_reader:
                    COUNTRY = row[0].split("(")[0].replace("'","")
                    YEAR = row[1]
                    BOTH_SEXES = row[2] if len(row[2]) != 0 else "NULL"
                    MALE = row[3] if len(row[3]) != 0 else "NULL"
                    FEMALE = row[4] if len(row[4]) != 0 else "NULL"
                    outfile.write("INSERT INTO " + TABLE_NAME + " VALUES (" + str(hiID) + "," + "'" + COUNTRY + "'" + "," + YEAR + "," + BOTH_SEXES + "," + MALE + "," + FEMALE + ");" + "\n")
                    countryfile.write("INSERT INTO " + "COUNTRY" + " VALUES (" + "'" + COUNTRY + "'" + ");" + "\n")
                    yearfile.write("INSERT INTO " + "TIME_YEAR" + " VALUES (" + YEAR + ");" + "\n")
                    hiID += 1