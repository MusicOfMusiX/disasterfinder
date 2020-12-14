"""
CSC110 Fall 2020 Project - model.py

Description
############################
This module provides a Neural Network Model class for:
    - creating a tensorflow.keras.Sequential 1-hidden-layer model
    - training a model with data from process_dataset1.py and process_dataset2.py
    - providing an interface for predicting the peak and longevity values for
        a given set of parameters (season, type, region), using a fully-trained model

This file is Copyright (c) 2020 Hyun Jo (Joshua) Jang.
"""
import random
from typing import List, Dict, Any
import tensorflow as tf
import numpy as np
import process_dataset1 as rd1
import process_dataset2 as rd2


class Model:
    """
    A Model class containing the actual tf.keras.Sequential neural network, as well as methods to interact with the nn.

    Instance Attributes:
        - target: the target output the model aims to predict. Either 'peak' or 'longevity'
        - rd1_data: the list of lists returned from process_dataset1.read_csv().
        - rd2_peak_dict: the dictionary of dictionaries returned from process_dataset2.read_csv(), first element.
        - rd2_longevity_dict: the dictionary of dictionaries returned from process_dataset2.read_csv(), second element.
        - train_inputs: numpy array of rd1_data, containing only the parameters required for the nn.
        - train_outputs: numpy array of peak or longevity values, corresponding to each row in train_inputs.
        - test_inputs: same as train_inputs, but on a smaller subset of rd1_data
            dedicated to testing the model's performance.
        - test_outputs: same as train_outputs, but on a smaller subset of rd1_data
            dedicated to testing the model's performance.
        - model: the Keras neural network.
    """
    target: str  # 'peak' or 'longevity'

    rd1_data: List[List[Any]]
    rd2_peak_dict: Dict[int, Dict[int, int]]
    rd2_longevity_dict: Dict[int, Dict[int, int]]

    train_inputs: np.array
    train_outputs: np.array
    test_inputs: np.array
    test_outputs: np.array

    model: tf.keras.Sequential

    def __init__(self, _target: str) -> None:
        """
        set target value,
        read data from DATASET1.csv and DATASET2.csv,
        ,populate all numpy array instance attributes,
        and configure the neural network, ready for training.

        Preconditions:
            - _target in ['peak', 'longevity']
        """
        self.target = _target

        self.rd1_data = rd1.read_csv("data/DATASET1.csv", cutoff=3000)
        self.rd2_peak_dict, self.rd2_longevity_dict = rd2.read_csv("data/DATASET2.csv")

        self._generate_sets()
        self._build()

    def train(self, _epochs=10) -> tf.keras.callbacks.History:
        """
        Train the neural network with the train_inputs and train_outputs,
        across a set number of epochs, default 10,
        and return the log of loss/error history, used for graphing later on.

        Preconditions:
            - epochs > 0
        """
        return self.model.fit(self.train_inputs, self.train_outputs, epochs=_epochs)

    def test(self) -> None:
        """
        Test the neural network's performance after training, using test_inputs and test_outputs.
        """
        self.model.evaluate(self.test_inputs, self.test_outputs)

    def predict(self, inputs: List[List[float]]) -> List[List[float]]:
        """
        For a given set of parameters in list of lists form,
        convert the above into numpy arrays,
        predict outputs using the trained neural network,
        and convert the resulting numpy array back into a Python list of lists.

        Preconditions:
            - inputs != []
        """
        result = self.model.predict(np.array(inputs))
        return result.tolist()

    def _build(self) -> None:
        """
        Configure the neural network,
        and compile it, ready for training.

        Current specifications:
            - Single hidden layers with 64 nodes, relu activation function.
            - Mean Absolute Error (MAE), as this is a regression problem.
                - Could use Mean Squared Error or any other alternative as well.
            - Adam optimiser. Chosen after experimenting with various optimisers.
        """
        self.model = tf.keras.Sequential([
            tf.keras.layers.Flatten(input_shape=(15,)),
            tf.keras.layers.Dense(64, activation='relu'),
            # tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1)
        ])

        self.model.compile(
            optimizer=tf.optimizers.Adam(learning_rate=0.001),
            loss='mean_absolute_error')

    def _generate_sets(self, test_num=200) -> None:
        """
        Convert Python list-of-list-form inputs into numpy arrays usable by Keras,
        and find corresponding output peak/longevity values for each set of parameters/inputs using _find_outputs().

        test_num indicates how many test inputs and outputs are to be extracted from DATASET1.
        """
        test_inputs = random.sample(self.rd1_data, test_num)
        train_inputs = [row for row in self.rd1_data if row not in test_inputs]

        test_outputs = self._find_outputs(test_inputs)
        train_outputs = self._find_outputs(train_inputs)

        self.test_inputs = np.array(self._remove_year_month(test_inputs))
        self.train_inputs = np.array(self._remove_year_month(train_inputs))
        self.test_outputs = np.array(test_outputs)
        self.train_outputs = np.array(train_outputs)

    def _find_outputs(self, input_list: List[List[int]]) -> List[int]:
        """
        Find corresponding peak/longevity values for each row of parameters in input_list.
        rd2_XXX_dict being dictionaries make the value retrieval process easier.

        Preconditions:
            - input_list != []
        """
        output_list = []

        if self.target == 'peak':
            for row in input_list:
                output_list.append(self.rd2_peak_dict[row[0]][row[1]])  # row[0] = year, row[1] = month
        elif self.target == 'longevity':
            for row in input_list:
                output_list.append(self.rd2_longevity_dict[row[0]][row[1]])

        return output_list

    def _remove_year_month(self, input_list: List[List[Any]]) -> List[Any]:
        """
        Input type is: List[List[int, int, List[float]]].
        Return type is: List[List[float]].
        Using Any for return type because typing thinks this is returning a 1-D list because of base_list = [].

        A single row from the raw list of lists from process_dataset1.read_csv was in the format:
        [year, month, [season, dtype, region, deaths, affected]].
        Since year and month are irrelevant to the neural network, this helper function removes them.

        Preconditions:
            - input_list != []
        """
        base_list = []
        for row in input_list:
            base_list.append(row[2])

        return base_list


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports':
            ['python_ta.contracts', 'process_dataset1', 'process_dataset2', 'random', 'tensorflow', 'numpy'],
        'max-line-length': 200,
        'allowed-io': [],
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)
