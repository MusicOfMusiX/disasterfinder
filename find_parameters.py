"""
CSC110 Fall 2020 Project - find_parameters.py

Description
############################
This module provides function definitions for:
    - generating input parameter sets of all possible combinations of seasons, types, and regions.
    - using a fully-trained neural network to predict and identify which set of parameters produce best peaks/longevity.

This file is Copyright (c) 2020 Hyun Jo (Joshua) Jang.
"""

from typing import List, Tuple
import model as m


def find_best_parameters(model: m.Model) -> List[Tuple[str, str, str]]:
    """
    The purpose of this function is to produce a wide range of hypothetical disaster scenarios,
    which are to be input into the trained neural network and evaluated of their outputs.

    Iterate through 25 combinations of deaths and affected values.
    For each iteration:
        - produce 80 inputs, with different parameters,
        - evaluate the peak or longevity (depending on which nn/model is input),
        - choose the single input (set of parameters) which produced best peak/longevity.
    Return the list of 'best performing' parameters for each death-affected iteration.

    Examples:
        - "when deaths=100, affected=1000, a STORM in AFRICA during SUMMER produced best peak interest"
        - "when deaths=0, affected=2000, a FLOOD in EUROPE during FALL produced best interest longevity"
    """
    parameters_list = []

    for deaths_i in range(0, 5):
        for affected_i in range(0, 5):
            batch = _generate_sets(deaths_i * 200, affected_i * 2000)
            results = model.predict(batch)
            best_index = _find_best_index(results)
            # print(_decode_features(batch[best_index]))
            parameters_list.append(_decode_features(batch[best_index]))

    return parameters_list


def _generate_sets(deaths: int, affected: int) -> List[List[int]]:
    """
    Produce 4 * 4 * 5 = 80 inputs for a model covering all possible combinations of parameters.
    This is for a fixed pair of deaths and affected values.
    """
    data_list = []
    for season in _one_hot_preset(4):
        for dtype in _one_hot_preset(4):
            for region in _one_hot_preset(5):
                data_list.append(season + dtype + region + [deaths] + [affected])

    return data_list  # total 80 rows.


def _find_best_index(results: List[List[float]]) -> int:
    """
    From a list of outputs (peak or longevity), find the index which leads to the maximum value.

    Preconditions
        - results != []

    >>> _find_best_index([[1], [2], [0]])
    1
    """
    current_max = 0
    max_index = -1
    for i in range(len(results)):
        if results[i][0] > current_max:
            current_max = results[i][0]
            max_index = i

    return max_index


def _one_hot_preset(n: int) -> List[List[int]]:
    """
    Return a list of possible one-hot arrays for two sizes: 4 and 5.

    Preconditions:
        - n in [4, 5]
    """
    if n == 4:
        return [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    if n == 5:
        return [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]]


def _decode_features(features: List[int]) -> Tuple[str, str, str]:
    """
    Convert one-hot encoded parameters into human-readable text format.

    Precondition:
        - len(features) == 13

    >>> _decode_features([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0])
    ('Winter', 'Flood', 'Europe')
    """
    one_hots = [features[0:4], features[4:8], features[8:13]]

    season_lookup = ['Winter', 'Spring', 'Summer', 'Fall']
    dtype_lookup = ['Wildfire', 'Flood', 'Storm', 'Earthquake']
    region_lookup = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']

    season = season_lookup[_one_hot_preset(4).index(one_hots[0])]
    dtype = dtype_lookup[_one_hot_preset(4).index(one_hots[1])]
    region = region_lookup[_one_hot_preset(5).index(one_hots[2])]

    return season, dtype, region


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports':
            ['python_ta.contracts', 'model'],
        'max-line-length': 200,
        'allowed-io': [],
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)
