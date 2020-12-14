"""
CSC110 Fall 2020 Project - process_dataset1.py

Description
############################
This module provides function definitions for:
    - reading rows off from data/DATASET1.csv
    - converting disaster parameters (season, type, region) into one-hot vectors
    - normalising # of deaths and affected into z-scores (0~1)
    - creating a list of lists containing such data.

This file is Copyright (c) 2020 Hyun Jo (Joshua) Jang.
"""

import csv
from typing import List, Any


def read_csv(filepath: str, cutoff=4500) -> List[List[Any]]:
    """
    Return type is: List[List[int, int, List[float]]].
    Using Any as the typing module doesn't like having more than one data type in a List[].

    Read rows from csv,
    convert parameters into one-hots,
    normalise deaths and affected values,
    and produce list of lists containing all of the above.

    cutoff determines how many rows are to be included in the final list, default 4500 out of 46XX rows.

    Formatting of a single row in the final returned List: [year, month, [season, dtype, region, deaths, affected]],
    where all discrete/categorical data are one-hot encoded, and continuous data are normalised.

    Preconditions:
        - filepath != None
        - cutoff > 0

    >>> import math
    >>> ll = read_csv('data/DATASET1.csv')
    >>> ll[0]
    [2010, 1, [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1.0, 0.027611940298507463]]
    """

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
            deaths = _normalise_number(int(row[4]), 222570)
            # row[5] corresponds to the pure # of affected but not dead. Not used in this program.
            affected = _normalise_number(int(row[6]), 134000000)

            data.append([year, month, season + dtype + region + [deaths] + [affected]])

    return data[:cutoff]


def _classify_season(month: int) -> List[float]:
    """
    Bin a given int month value into 4 categories/seasons,
    and return a one-hot vector representation of it.

    Winter: months 12, 1, 2
    Spring: months 3, 4, 5
    Summer: months 6, 7, 8
    Fall: months 9, 10, 11

    Preconditions:
        - 1 <= month <= 12
    """
    if 12 <= month <= 2:
        return [1, 0, 0, 0]
    elif 3 <= month <= 5:
        return [0, 1, 0, 0]
    elif 6 <= month <= 8:
        return [0, 0, 1, 0]
    else:
        return [0, 0, 0, 1]


def _classify_and_convert(name: str, lookup: List[str]) -> List[float]:
    """
    For disaster type (4 categories) and region (5 categories).
    Receives a name and a lookup list of names,
    and generates a corresponding one-hot vector of the name.

    Preconditions:
        - name in lookup

    >>> _classify_and_convert('Flood', ['Wildfire', 'Flood', 'Storm', 'Earthquake'])
    [0, 1, 0, 0]
    """
    n = len(lookup)
    one_hot = []
    for i in range(n):
        if i == lookup.index(name):
            one_hot.append(1)
        else:
            one_hot.append(0)

    return one_hot


def _normalise_number(number: int, maximum: int) -> float:
    """
    Produce a z-score value for the corresponding # of deaths or affected input.

    The maximum # of deaths in DATASET1.csv is 222570,
    the maximum # of affected in DATASET1.csv is 134000000.

    Resulting value is 0 to 1, inclusive.

    Preconditions:
        - 0 <= deaths <= maximum
        - maximum in [222570, 134000000]
    """
    return number / maximum


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'csv'],
        'max-line-length': 200,
        'allowed-io': ['read_csv'],
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)
