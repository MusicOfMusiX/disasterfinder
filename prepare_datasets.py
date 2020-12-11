import read_dataset1 as rd1
import read_dataset2 as rd2
import numpy as np
import random
from typing import List, Tuple

# split training and test data here
# convert lists into numpy arrays here

rd1_data = rd1.read_csv_raw("data/DATASET1_FULL.csv")
rd2_data = rd2.convert_to_dict(rd2.read_csv_raw("data/DATASET2_FULL.csv"))


def generate_sets(test_num=250) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    # why i need to add 4 np.ndarrays? no idea.

    test_inputs = random.sample(rd1_data, test_num)
    train_inputs = [row for row in rd1_data if row not in test_inputs]

    test_outputs = find_outputs(test_inputs)
    train_outputs = find_outputs(train_inputs)

    test_inputs = np.array(test_inputs)
    train_inputs = np.array(train_inputs)
    test_outputs = np.array(test_outputs)
    train_outputs = np.array(train_outputs)

    return train_inputs, train_outputs, test_inputs, test_outputs

    #print(test_inputs.shape)
    #print(test_outputs.shape)
    #print(train_inputs.shape)
    #print(train_outputs.shape)


def find_outputs(data: List[List[int]]) -> List[List[int]]:
    outputlist = []
    for row in data:
        outputlist.append(rd2_data[row[0]][row[1]])

    return outputlist

