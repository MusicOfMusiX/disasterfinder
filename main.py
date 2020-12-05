import tensorflow as tf
from tensorflow import keras
import numpy as np

import dataset1_process
import dataset2_process

if __name__ == '__main__':
    # print("TF version: " + tf.__version__)
    rows = dataset1_process.read_csv_raw('data/DATASET1_FULL.csv')
    dataset1_process.print_row(rows[2000])

