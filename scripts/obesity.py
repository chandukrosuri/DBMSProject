# Import libraries
import sys
import csv
import os

data = "../data/obesity.csv"
sql = "../sql_commands/obesity.sql"

TABLE_NAME = "OBESITY"

# Create .sql file for obesity 
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
        # Skip next few rows 
        next(csv_reader)
        next(csv_reader)
        next(csv_reader)

        # Each preceding row contains country information
        for row in csv_reader:
            COUNTRY = row[0].split("(")[0]
            row = row[1:] # Subset the row to remove first element
            year_counter = 0
            for i in range(len(row)):
                if (i % 3) == 0:
                    BOTH_SEXES = row[i].split(" ")[0]
                if (i % 3) == 1:
                    MALE = row[i].split(" ")[0]
                if (i % 3) == 2:
                    FEMALE = row[i].split(" ")[0]
                    YEAR = str(int_years[year_counter])
                    outfile.write("INSERT INTO " + TABLE_NAME + " (" + COUNTRY + "," + YEAR + "," + BOTH_SEXES + "," + MALE + "," + FEMALE + ");" + "\n")
                    year_counter += 1

           