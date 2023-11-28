# Import libraries
import sys
import csv
import os

data = "../data/government_debt.csv"
sql = "../sql_commands/government_debt.sql"
country_sql = "../sql_commands/government_debt_country.sql"
year_sql = "../sql_commands/government_debt_year.sql"

TABLE_NAME = "GOVERNMENT_DEBT"

# Create .sql file for government debt 
with open(data, 'r') as infile:
    with open(sql, 'w') as outfile:
        with open(country_sql, 'w') as countryfile:
            with open(year_sql, 'w') as yearfile:
                csv_reader = csv.reader(infile)
                # First line is all the years. Have to do some preprocessing.
                years = list(set(next(csv_reader)))
                int_years = []
                for year in years:
                    if year.isdigit():
                        int_years.append(int(year))
                # Sort the int years in descending order to get same ordering
                int_years.sort()
                # print(int_years)
                # Skip next few rows 
                next(csv_reader)

                # Each preceding row contains country information
                hiID = 0
                for row in csv_reader:
                    COUNTRY = row[0].split("(")[0].replace("'","").split(",",1)[0]
                    if len(COUNTRY) == 0:
                        break
                    row = row[1:] # Subset the row to remove first element
                    for i in range(len(row)):
                        YEAR = str(int_years[i])
                        DEBT = row[i] if row[i] != "no data" else "NULL"
                        outfile.write("INSERT INTO " + TABLE_NAME + " VALUES (" + str(hiID) + "," + "'" + COUNTRY + "'" + "," + YEAR + "," + DEBT + ");" + "\n")
                        countryfile.write("INSERT INTO " + "COUNTRY" + " VALUES (" + "'" + COUNTRY + "'" + ");" + "\n")
                        yearfile.write("INSERT INTO " + "TIME_YEAR" + " VALUES (" + YEAR + ");" + "\n")
                        hiID += 1
