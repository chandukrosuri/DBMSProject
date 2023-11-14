# Import libraries
import sys
import csv
import os

data = "../data/mean-years-of-schooling-long-run.csv"
sql = "../sql_commands/schooling.sql"

TABLE_NAME = "AVERAGE_SCHOOLING_YEARS"

# Create .sql file for average schooling
with open(data, 'r') as infile:
    with open(sql, 'w') as outfile:
        csv_reader = csv.reader(infile)
        # Skip the first two header rows
        next(csv_reader)
        for row in csv_reader:
            row = row[0].split(";")
            COUNTRY = row[0].split("(")[0]
            YEAR = row[2]
            SCHOOLING = row[3] if len(row[3]) != 0 else "NULL"
            outfile.write("INSERT INTO " + TABLE_NAME + " VALUES (" + COUNTRY + "," + YEAR + "," + SCHOOLING + ");" + "\n")
           