import csv
from typing import List, Dict

# calculate peak and longevity values here.
# final data array: [year, month, peak, longevity]


def read_csv_raw(filepath: str) -> List[List[int]]:
    with open(filepath) as file:
        reader = csv.reader(file)
        next(reader)

        data = []

        for row in reader:
            # row is a list of strings
            year = int(row[0])
            month = int(row[1])
            peak = int(row[2]) + int(row[3])

            data.append([year, month, peak])

        data = calculate_longevity(data)

    return data


# no need to calculate peak, peak is just the value @ date.
# min longevity = 1 month
# max longevity = 3 months
# if next month value > current peak, longevity = 1
# longevity is cut off when decreased > 30%
# September 2020 is the final month.

def calculate_longevity(data: List[List[int]]) -> List[List[int]]:
    for stat_index in range(0, len(data) - 2):
        count = 1
        peak = float(data[stat_index][2])

        for i in range(1, 3):
            if peak * 0.7 <= data[stat_index + i][2] <= peak:
                count += 1

        data[stat_index].append(count)

    return data[:-2]


def convert_to_dict(datalist: List[List[int]]) -> Dict[int, Dict[int, List[int]]]:
    datadict = {}
    # Add initial keys to avoid keyerror.
    for year in range(2004, 2021):
        datadict[year] = {}

    for row in datalist:
        datadict[row[0]][row[1]] = [row[2], row[3]]

    return datadict
