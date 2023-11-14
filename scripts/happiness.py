# Import libraries
import sys
import csv
import os

data = "../data/happiness-cantril-ladder.csv"
sql = "../sql_commands/happiness.sql"

TABLE_NAME = "HAPPINESS"

# Create .sql file for average schooling
with open(data, 'r') as infile:
    with open(sql, 'w') as outfile:
        csv_reader = csv.reader(infile)
        # Skip the first two header rows
        next(csv_reader)
        for row in csv_reader:
            COUNTRY = row[0].split("(")[0]
            CODE = row[1] if len(row[1]) != 0 else "NULL"
            YEAR = row[2] if len(row[2]) != 0 else "NULL"
            CANTRIL = row[3] if len(row[3]) != 0 else "NULL"
            outfile.write("INSERT INTO " + TABLE_NAME + " VALUES (" + COUNTRY + "," + YEAR + "," + CANTRIL + "," + CODE + ");" + "\n")
           