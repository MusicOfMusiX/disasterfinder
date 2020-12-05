import csv
from typing import List


def read_csv_raw(filepath: str) -> List[List[int]]:
    # remember, everything in the csv are strings, convert them.

    with open(filepath) as file:
        reader = csv.reader(file)
        reader.next()

        data = []
        for row in reader:
            # row is a list of strings
            year = int(row[2])
            month = int(row[3])
            dtype = classify_dtype(row[0])  # disaster type
            region = classify_region(row[1])
            deaths = int(row[4])
            affected = int(row[6])  # total affected, not affected only.

            data.append([year, month, dtype, region, deaths, affected])

    return data


def classify_dtype(name: str) -> int:
    # converts string disaster type names into integers of 0~3 according to the specifications.
    lookup = ['Wildfire', 'Flood', 'Storm', 'Earthquake']
    return lookup.index(name)


def classify_region(name: str) -> int:
    # converts string region names into integers of 0~4 according to the specifications.
    lookup = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']
    return lookup.index(name)


def print_row(row: List[int]) -> None:
    print("Year-Month: %d-%d" % (row[0], row[1]))
    print("Type: %s" % row[2])
    print("Region: %s" % row[3])
    print("Deaths-Affected: %d-%d" % (row[4], row[5]))
