import process_dataset1 as rd1
import process_dataset2 as rd2
import random
from typing import List, Dict, Any
import tensorflow as tf
import numpy as np

# the input array, with all categories one-hot encoded, will have dimension (n, 15).


class Model:
    target: str  # 'peak' or 'longevity'

    rd1_data: List[List[Any]]
    rd2_peak_dict: Dict[int, Dict[int, int]]
    rd2_longevity_dict: Dict[int, Dict[int, int]]

    train_inputs: np.array
    train_outputs: np.array
    test_inputs: np.array
    test_outputs: np.array

    model: tf.keras.Sequential

    def __init__(self, _target: str):
        self.target = _target

        self.rd1_data = rd1.read_csv("data/DATASET1_FULL.csv", cutoff=3000)
        self.rd2_peak_dict, self.rd2_longevity_dict = rd2.read_csv("data/DATASET2_FULL.csv")

        self._generate_sets()
        self._build()

    def train(self) -> tf.keras.callbacks.History:
        return self.model.fit(self.train_inputs, self.train_outputs, epochs=60)

    def test(self) -> None:
        self.model.evaluate(self.test_inputs, self.test_outputs)

    def predict(self, inputs: List[List[float]]) -> List[List[float]]:
        result = self.model.predict(np.array(inputs))
        return result.tolist()

    def _build(self) -> None:
        self.model = tf.keras.Sequential([
            tf.keras.layers.Flatten(input_shape=(15,)),
            # tf.keras.layers.Dense(64, activation='relu'),
            # tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1)
        ])

        self.model.compile(
            optimizer=tf.optimizers.Adam(learning_rate=0.005),
            loss='mean_absolute_error')

    def _generate_sets(self, test_num=200) -> None:
        test_inputs = random.sample(self.rd1_data, test_num)
        train_inputs = [row for row in self.rd1_data if row not in test_inputs]

        test_outputs = self._find_outputs(test_inputs)
        train_outputs = self._find_outputs(train_inputs)

        self.test_inputs = np.array(self._remove_year_month(test_inputs))
        self.train_inputs = np.array(self._remove_year_month(train_inputs))
        self.test_outputs = np.array(test_outputs)
        self.train_outputs = np.array(train_outputs)

    def _find_outputs(self, data: List[List[int]]) -> List[int]:
        output_list = []

        if self.target == 'peak':
            for row in data:
                output_list.append(self.rd2_peak_dict[row[0]][row[1]])
        elif self.target == 'longevity':
            for row in data:
                output_list.append(self.rd2_longevity_dict[row[0]][row[1]])

        return output_list

    def _remove_year_month(self, input_list: List[List[Any]]) -> List[Any]:
        # List[List[Any]] = List[List[int, int, List[float]]]
        # This returns List[List[float]].
        # Using Any because typing thinks I am going to return a 1-D list because of base_list = [].
        base_list = []
        for row in input_list:
            base_list.append(row[2])

        return base_list
