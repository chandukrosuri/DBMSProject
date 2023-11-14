# Import libraries
import sys
import csv
import os

data = "../data/death-rates-from-air-pollution.csv"
sql = "../sql_commands/air_pollution_deaths.sql"

TABLE_NAME = "DEATHS_DUETO_AIRPOLLUTION"

# Create .sql file for air pollution deaths
with open(data, 'r') as infile:
    with open(sql, 'w') as outfile:
        csv_reader = csv.reader(infile)
        # Skip the first two header rows
        next(csv_reader)
        for row in csv_reader:
            COUNTRY = row[0].split("(")[0]
            YEAR = row[2]
            TOTAL = row[3] if len(row[3]) != 0 else "NULL"
            INDOOR = row[4] if len(row[4]) != 0 else "NULL"
            OUTDOOR = row[5] if len(row[4]) != 0 else "NULL"
            outfile.write("INSERT INTO " + TABLE_NAME + " VALUES (" + COUNTRY + "," + YEAR + "," + OUTDOOR + "," + INDOOR + "," + TOTAL + ");" + "\n")
           