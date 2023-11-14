# Import libraries
import sys
import csv
import os

data = "../data/basic_sanitation.csv"
sql = "../sql_commands/basic_sanitation.sql"

TABLE_NAME = "ACCESS_TO_BASIC_SANITIZATION"

# Create .sql file for basic sanitation 
with open(data, 'r') as infile:
    with open(sql, 'w') as outfile:
        csv_reader = csv.reader(infile)
        # First line is all the years. Have to do some preprocessing.
        years = list(set(next(csv_reader)))
        int_years = []
        for year in years:
            if len(year) != 0:
                int_years.append(int(year))
        # Sort the int years in descending order to get same ordering
        int_years.sort(reverse = True)
        # print(int_years)
        # Skip next few rows 
        next(csv_reader)
        next(csv_reader)

        # Each preceding row contains country information
        for row in csv_reader:
            COUNTRY = row[0].split("(")[0]
            row = row[1:] # Subset the row to remove first element
            year_counter = 0
            for i in range(len(row)):
                if (i % 6) == 0:
                    TOTAL = row[i].split(" ")[0] if len(row[i].split(" ")[0]) != 0 else "NULL"
                if (i % 6) == 1:
                    URBAN = row[i].split(" ")[0] if len(row[i].split(" ")[0]) != 0 else "NULL"
                if (i % 6) == 2:
                    RURAL = row[i].split(" ")[0] if len(row[i].split(" ")[0]) != 0 else "NULL"
                    YEAR = str(int_years[year_counter])
                    outfile.write("INSERT INTO " + TABLE_NAME + " VALUES (" + COUNTRY + "," + YEAR + "," + RURAL + "," + URBAN + "," + TOTAL + ");" + "\n")
                    year_counter += 1

           