import model as m
from typing import List, Tuple


def find_best_parameters(model: m.Model) -> List[Tuple[str, str, str]]:
    parameters_list = []

    for deaths_i in range(0, 5):
        for affected_i in range(0, 5):
            batch = _generate_sets(deaths_i*200, affected_i*2000)
            results = model.predict(batch)
            best_index = _find_best_index(results)
            # print(_decode_features(batch[best_index]))
            parameters_list.append(_decode_features(batch[best_index]))

    return parameters_list


def _generate_sets(deaths: int, affected: int) -> List[List[int]]:
    data_list = []
    for season in _one_hot_preset(4):
        for dtype in _one_hot_preset(4):
            for region in _one_hot_preset(5):
                data_list.append(season + dtype + region + [deaths] + [affected])

    return data_list  # total 80 rows.


def _find_best_index(results: List[List[float]]) -> int:
    current_max = 0
    max_index = -1
    for i in range(len(results)):
        if results[i][0] > current_max:
            current_max = results[i][0]
            max_index = i

    return max_index


def _one_hot_preset(n: int) -> List[List[int]]:
    if n == 4:
        return [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    if n == 5:
        return [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]]


def _decode_features(features: List[int]):
    one_hots = [features[0:4], features[4:8], features[8:13]]

    season_lookup = ['Winter', 'Spring', 'Summer', 'Fall']
    dtype_lookup = ['Wildfire', 'Flood', 'Storm', 'Earthquake']
    region_lookup = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']

    season = season_lookup[_one_hot_preset(4).index(one_hots[0])]
    dtype = dtype_lookup[_one_hot_preset(4).index(one_hots[1])]
    region = region_lookup[_one_hot_preset(5).index(one_hots[2])]

    return season, dtype, region

