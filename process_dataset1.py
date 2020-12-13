import csv
from typing import List, Any

# data array: [year, month, [season + type + region + deaths + affected]]


def read_csv(filepath: str) -> List[List[Any]]:  # Any can be an int (year-month) or a list.
    # remember, everything in the csv are strings, convert them.

    with open(filepath) as file:
        reader = csv.reader(file)
        next(reader)

        data = []
        for row in reader:
            # row is a list of strings
            year = int(row[2])
            month = int(row[3])
            season = _classify_season(month)
            dtype = _classify_and_convert(row[0], ['Wildfire', 'Flood', 'Storm', 'Earthquake'])
            region = _classify_and_convert(row[1], ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania'])
            deaths = _normalise_deaths(int(row[4]))
            affected = _normalise_affected(int(row[6]))  # total affected, not affected only.

            data.append([year, month, season + dtype + region + [deaths] + [affected]])

    return data


def _classify_season(month: int) -> List[float]:
    if 12 <= month <= 2:
        return [1, 0, 0, 0]
    elif 3 <= month <= 5:
        return [0, 1, 0, 0]
    elif 6 <= month <= 8:
        return [0, 0, 1, 0]
    else:
        return [0, 0, 0, 1]


def _classify_and_convert(name: str, lookup: List[str]) -> List[float]:
    n = len(lookup)
    one_hot = []
    for i in range(n):
        if i == lookup.index(name):
            one_hot.append(1)
        else:
            one_hot.append(0)

    return one_hot


def _normalise_deaths(deaths: int) -> float:
    return deaths / 222570


def _normalise_affected(affected: int) -> float:
    return affected / 134000000
