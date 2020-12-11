import csv
from typing import List


# data array: [year, month, season, type, region, deaths, affected]
# final data map: {year: {month: (peak, longevity)}}

def read_csv_raw(filepath: str) -> List[List[int]]:
    # remember, everything in the csv are strings, convert them.

    with open(filepath) as file:
        reader = csv.reader(file)
        next(reader)

        data = []
        for row in reader:
            # row is a list of strings
            year = int(row[2])
            month = int(row[3])
            season = classify_season(month)
            dtype = classify_dtype(row[0])  # disaster type
            region = classify_region(row[1])
            deaths = int(row[4])
            affected = int(row[6])  # total affected, not affected only.

            data.append([year, month, season, dtype, region, deaths, affected])

    return data


def classify_season(month: int) -> int:
    if 12 <= month <= 2:
        return 0
    elif 3 <= month <= 5:
        return 1
    elif 6 <= month <= 8:
        return 2
    else:
        return 3


def classify_dtype(name: str) -> int:
    # converts string disaster type names into integers of 0~3 according to the specifications.
    lookup = ['Wildfire', 'Flood', 'Storm', 'Earthquake']
    return lookup.index(name)


def classify_region(name: str) -> int:
    # converts string region names into integers of 0~4 according to the specifications.
    lookup = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']
    return lookup.index(name)
