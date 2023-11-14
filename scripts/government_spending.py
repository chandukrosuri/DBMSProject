# Import libraries
import sys
import csv
import os

data = "../data/historical-gov-spending-gdp.csv"
sql = "../sql_commands/gov_spending.sql"

TABLE_NAME = "GOVERNMENT_EXPENDITURE"

# Create .sql file for government spending
with open(data, 'r') as infile:
    with open(sql, 'w') as outfile:
        csv_reader = csv.reader(infile)
        # Skip the first two header rows
        next(csv_reader)
        for row in csv_reader:
            COUNTRY = row[0].split("(")[0]
            YEAR = row[2] if len(row[2]) != 0 else "NULL"
            GDP_SPENDING = row[3] if len(row[3]) != 0 else "NULL"
            outfile.write("INSERT INTO " + TABLE_NAME + " VALUES (" + COUNTRY + "," + YEAR + "," + GDP_SPENDING + ");" + "\n")
           