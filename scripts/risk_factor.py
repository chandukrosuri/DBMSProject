# Import libraries
import sys
import csv
import os

data = "../data/number-of-deaths-by-risk-factor.csv"
sql = "../sql_commands/risk_factor.sql"

TABLE_NAME = "DEATHS_BY_RISKFACTOR"

# Create .sql file for risk factor deaths
with open(data, 'r') as infile:
    with open(sql, 'w') as outfile:
        csv_reader = csv.reader(infile)
        # Skip the first two header rows
        next(csv_reader)
        for row in csv_reader:
            COUNTRY = row[0].split("(")[0]
            YEAR = row[1]
            WATER = row[2] if len(row[2]) != 0 else "NULL"
            SANITATION = row[3] if len(row[3]) != 0 else "NULL"
            AIRPOLLUTION = row[5] if len(row[5]) != 0 else "NULL"
            CHILDWASTING = row[8] if len(row[8]) != 0 else "NULL"
            CHILDSTUNTING = row[9] if len(row[9]) != 0 else "NULL"
            outfile.write("INSERT INTO " + TABLE_NAME + " (" + COUNTRY + "," + YEAR + "," + WATER + "," + SANITATION + "," + CHILDWASTING + "," + CHILDSTUNTING + "," + AIRPOLLUTION + ");" + "\n")
           