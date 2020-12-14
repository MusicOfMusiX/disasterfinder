"""
CSC110 Fall 2020 Project - process_dataset2.py

Description
############################
This module provides function definitions for:
    - reading rows off from data/DATASET2.csv
    - creating two dictionary of dictionaries containing values for:
        - peak interest, accessible via dict[year][month]
        - interest longevity, accessible via dict[year][month]

This file is Copyright (c) 2020 Hyun Jo (Joshua) Jang.
"""

import csv
from typing import List, Dict, Tuple


def read_csv(filepath: str) -> Tuple[Dict[int, Dict[int, int]], Dict[int, Dict[int, int]]]:
    """
    Read rows from csv,
    calculate combined peak values for both keywords: 'Climate' and 'Climate Change',
    generate longevity values ranging from 1 to 3, inclusive,
    and generate two dictionary of dictionaries to store both sets of values separately.

    Peak values range roughly from 20 to 70,
    Longevity values are either 1, 2, or 3 (months).
    The two values are not normalised in any way.

    Note that a 'peak' value for a specific year-month date is simply the interest value at such date.

    Formatting of final returned Tuple: {year: {month: peak}}, {year: {month: longevity}}

    Preconditions:
        - filepath != None

    >>> dd1, dd2 = read_csv('data/DATASET2.csv')
    >>> dd1[2014][8]
    37
    >>> dd2[2020][6]
    3
    """
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


def _calculate_longevity(data: List[List[int]]) -> List[List[int]]:
    """
    With given list of peak interest values in chronological order,
    find interest longevity values for each year-month date,
    append the new values to the original data list,
    and return it.

    Specifications:
        - longevity is the measure of how long the peak of a certain month is maintained
            over the course of following months.
        - minimum longevity = 1 month
        - maximum longevity = 3 months
        - if next month value > current peak, longevity = 1
        - when the following months' interest value is higher than 70% of the original month's value,
            it is considered that the original interest is maintained.
        - September 2020 is the final month which has longevity data,
            since October and November must be used in calculation.

    Formatting fo a row in the input List: [year, month, peak].
    Formatting of a row in the final returned List: [year, month, peak, longevity].

    Preconditions:
        - data != []

    >>> ll = _calculate_longevity([[2020, 6, 30], [2020, 7, 27], [2020, 8, 10]])
    >>> ll
    [[2020, 6, 30, 2]]
    """
    for stat_index in range(0, len(data) - 2):
        count = 1
        peak = float(data[stat_index][2])

        for i in range(1, 3):
            if peak * 0.7 <= data[stat_index + i][2] <= peak:
                count += 1

        data[stat_index].append(count)

    return data[:-2]


def _convert_to_dict(data_list: List[List[int]]) -> Tuple[Dict[int, Dict[int, int]], Dict[int, Dict[int, int]]]:
    """
    Take a list of lists containing peak and longevity values for each year-month date,
    and convert it into two dictionary of dictionaries for peak and longevity,
    both accessible via indexing with year and month.

    Formatting of a row in the input List: [year, month, peak, longevity].
    Formatting of final returned Tuple: {year: {month: peak}}, {year: {month: longevity}}

    preconditions:
        - data_list != []

    >>> dd1, dd2 = _convert_to_dict([[2020, 6, 30, 2]])
    >>> dd1[2020][6]
    30
    >>> dd2[2020][6]
    2
    """
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
