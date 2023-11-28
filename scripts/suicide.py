# Import libraries
import sys
import csv
import os

data = "../data/suicide_rate.csv"
sql = "../sql_commands/suicide.sql"
country_sql = "../sql_commands/suicide_country.sql"
year_sql = "../sql_commands/suicide_year.sql"

TABLE_NAME = "SUICIDE_RATE"

# Create .sql file for suicide deaths
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
                    YEAR = row[1]
                    SEX = row[2] if len(row[2]) != 0 else "NULL"
                    AGE = row[3].split(" ")[0].replace("+","") if len(row[3].split(" ")[0]) != 0 else "NULL"
                    SUICIDE_NO = row[4] if len(row[4]) != 0 else "NULL"
                    POPULATION = row[5] if len(row[5]) != 0 else "NULL"
                    GDP = row[9].replace(",","") if len(row[9]) != 0 else "NULL"
                    GENERATION = row[11] if (len(row[11])) != 0 else "NULL"
                    if AGE == "NULL":
                        outfile.write("INSERT INTO " + TABLE_NAME + " VALUES (" + str(hiID) + "," + "'" + COUNTRY + "'" + "," + YEAR + "," + "'" + SEX + "'" + "," + AGE + "," + SUICIDE_NO + "," + POPULATION + "," + GDP + "," + "'" + GENERATION + "'" + ");" + "\n")
                        countryfile.write("INSERT INTO " + "COUNTRY" + " VALUES (" + "'" + COUNTRY + "'" + ");" + "\n")
                        yearfile.write("INSERT INTO " + "TIME_YEAR" + " VALUES (" + YEAR + ");" + "\n")
                        hiID += 1
                    elif AGE == "75":
                        outfile.write("INSERT INTO " + TABLE_NAME + " VALUES (" + str(hiID) + "," + "'" + COUNTRY + "'" + "," + YEAR + "," + "'" + SEX + "'" + "," + AGE + "," + SUICIDE_NO + "," + POPULATION + "," + GDP + "," + "'" + GENERATION + "'" + ");" + "\n")
                        countryfile.write("INSERT INTO " + "COUNTRY" + " VALUES (" + "'" + COUNTRY + "'" + ");" + "\n")
                        yearfile.write("INSERT INTO " + "TIME_YEAR" + " VALUES (" + YEAR + ");" + "\n")
                        hiID += 1
                    else:
                        for age in range(int(AGE.split("-")[0]), int(AGE.split("-")[1])):
                            outfile.write("INSERT INTO " + TABLE_NAME + " VALUES (" + str(hiID) + "," + "'" + COUNTRY + "'" + "," + YEAR + "," + "'" + SEX + "'" + "," + str(age) + "," + SUICIDE_NO + "," + POPULATION + "," + GDP + "," + "'" + GENERATION + "'" + ");" + "\n")
                            countryfile.write("INSERT INTO " + "COUNTRY" + " VALUES (" + "'" + COUNTRY + "'" + ");" + "\n")
                            yearfile.write("INSERT INTO " + "TIME_YEAR" + " VALUES (" + YEAR + ");" + "\n")
                            hiID += 1