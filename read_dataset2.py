import csv
from typing import List


def read_csv_raw(filepath: str) -> List[List[int]]:
    with open(filepath) as file:
        reader = csv.reader(file)
        reader.next()

        data = []
        for row in reader:
            # row is a list of strings
            year = int(row[0])
            month = int(row[1])
            climatechangestat = int(row[2])
            climatestat = int(row[3])

            data.append([year, month, climatechangestat, climatestat])

    return data
