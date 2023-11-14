# Import libraries
import sys
import csv
import os

data = "../data/suicide_rate.csv"
sql = "../sql_commands/suicide.sql"

TABLE_NAME = "SUICIDE_RATE"

# Create .sql file for suicide deaths
with open(data, 'r') as infile:
    with open(sql, 'w') as outfile:
        csv_reader = csv.reader(infile)
        # Skip the first two header rows
        next(csv_reader)
        for row in csv_reader:
            COUNTRY = row[0].split("(")[0]
            YEAR = row[1]
            SEX = row[2] if len(row[2]) != 0 else "NULL"
            AGE = row[3].split(" ")[0] if len(row[3].split(" ")[0]) != 0 else "NULL"
            SUICIDE_NO = row[4] if len(row[4]) != 0 else "NULL"
            POPULATION = row[5] if len(row[5]) != 0 else "NULL"
            GDP = row[9].replace(",","") if len(row[9]) != 0 else "NULL"
            outfile.write("INSERT INTO " + TABLE_NAME + " VALUES (" + COUNTRY + "," + YEAR + "," + SEX + "," + AGE + "," + SUICIDE_NO + "," + POPULATION + "," + GDP + ");" + "\n")
           