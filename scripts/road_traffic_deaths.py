# Import libraries
import sys
import csv
import os

data = "../data/road_traffic_deaths.csv"
sql = "../sql_commands/road_traffic_deaths.sql"

TABLE_NAME = "ROAD_TRAFFIC_DEATH"

# Create .sql file for road_traffic_deaths
with open(data, 'r') as infile:
    with open(sql, 'w') as outfile:
        csv_reader = csv.reader(infile)
        # Skip the first two header rows
        next(csv_reader)
        next(csv_reader)
        for row in csv_reader:
            COUNTRY = row[0].split("(")[0]
            YEAR = row[1]
            BOTH_SEXES = row[2].split(" ")[0] if len(row[2].split(" ")[0]) != 0 else "NULL"
            MALE = row[3].split(" ")[0] if len(row[3].split(" ")[0]) != 0 else "NULL"
            FEMALE = row[4].split(" ")[0] if len(row[4].split(" ")[0]) != 0 else "NULL"
            outfile.write("INSERT INTO " + TABLE_NAME + " (" + COUNTRY + "," + YEAR + "," + BOTH_SEXES + "," + MALE + "," + FEMALE + ");" + "\n")
           