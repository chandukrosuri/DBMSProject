# Import libraries
import sys
import csv
import os

data = "../data/gdp_1960_2020.csv"
sql = "../sql_commands/gdp.sql"

TABLE_NAME = "GDP"

# Create .sql file for gdp
with open(data, 'r') as infile:
    with open(sql, 'w') as outfile:
        csv_reader = csv.reader(infile)
        # Skip the first two header rows
        next(csv_reader)
        for row in csv_reader:
            YEAR = row[0] if len(row[0]) != 0 else "NULL"
            RANK = row[1] if len(row[1]) != 0 else "NULL"
            COUNTRY = row[2].split("(")[0] if len(row[2].split("(")[0]) != 0 else "NULL"
            STATE = row[3] if len(row[3]) != 0 else "NULL"
            GDP = row[4] if len(row[4]) != 0 else "NULL"
            GDP_PERCENTAGE = row[5] if len(row[5]) != 0 else "NULL"
            outfile.write("INSERT INTO " + TABLE_NAME + " (" + COUNTRY + "," + YEAR + "," + RANK + "," + GDP_PERCENTAGE + "," + GDP + "," + STATE + ");" + "\n")
           