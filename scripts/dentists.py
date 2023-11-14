# Import libraries
import sys
import csv
import os

data = "../data/dentists.csv"
sql = "../sql_commands/dentists.sql"

TABLE_NAME = "NUMBER_OF_DENTISTS"

# Create .sql file for medical doctors
with open(data, 'r') as infile:
    with open(sql, 'w') as outfile:
        csv_reader = csv.reader(infile)
        # Skip the first two header rows
        next(csv_reader)
        for row in csv_reader:
            COUNTRY = row[0].split("(")[0]
            YEAR = row[1]
            NUM_DENTISTS = row[3] if len(row[3]) != 0 else "NULL"
            outfile.write("INSERT INTO " + TABLE_NAME + " (" + COUNTRY + "," + YEAR + "," + NUM_DENTISTS + ");" + "\n")
           