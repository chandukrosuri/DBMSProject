# Import libraries
import sys
import csv
import os

data = "../data/births_attended.csv"
sql = "../sql_commands/births_attended.sql"

TABLE_NAME = "BIRTHS_ATTENDEDBY_SKILLED_HEALTHPROFESSIONAL"

# Create .sql file for births attended
with open(data, 'r') as infile:
    with open(sql, 'w') as outfile:
        csv_reader = csv.reader(infile)
        # Skip the first two header rows
        next(csv_reader)
        for row in csv_reader:
            COUNTRY = row[0].split("(")[0]
            YEARS = row[1].split("-")
            BIRTHS = row[2] if len(row[2]) != 0 else "NULL"
            for YEAR in YEARS:
                outfile.write("INSERT INTO " + TABLE_NAME + " VALUES (" + COUNTRY + "," + YEAR + "," + BIRTHS + ");" + "\n")
           