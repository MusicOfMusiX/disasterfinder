import csv
from typing import List, Dict, Tuple

# data map: {year: {month: peak/longevity}}


def read_csv(filepath: str) -> Tuple[Dict[int, Dict[int, int]], Dict[int, Dict[int, int]]]:
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

    return _convert_to_dict(_calculate_longevity(data))


# no need to calculate peak, peak is just the value @ date.
# min longevity = 1 month
# max longevity = 3 months
# if next month value > current peak, longevity = 1
# longevity is cut off when decreased > 30%
# September 2020 is the final month.

def _calculate_longevity(data: List[List[int]]) -> List[List[int]]:
    for stat_index in range(0, len(data) - 2):
        count = 1
        peak = float(data[stat_index][2])

        for i in range(1, 3):
            if peak * 0.7 <= data[stat_index + i][2] <= peak:
                count += 1

        data[stat_index].append(count)

    return data[:-2]


def _convert_to_dict(data_list: List[List[int]]) -> Tuple[Dict[int, Dict[int, int]], Dict[int, Dict[int, int]]]:
    peak_dict = {}
    longevity_dict = {}
    # Add initial keys to avoid keyerror.
    for year in range(2004, 2021):
        peak_dict[year] = {}
        longevity_dict[year] = {}

    for row in data_list:
        peak_dict[row[0]][row[1]] = row[2]
        longevity_dict[row[0]][row[1]] = row[3]

    return peak_dict, longevity_dict
