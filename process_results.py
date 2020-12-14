"""
CSC110 Fall 2020 Project - process_results.py

Description
############################
This module provides function definitions for:
    - finding the SINGLE best performing set of parameters from the list of parameters returned by
        find_parameters.find_best_parameters()
    - displaying neural network training log
    - displaying the best set of parameters for each peak and longevity targets.

This file is Copyright (c) 2020 Hyun Jo (Joshua) Jang.
"""

from typing import List, Tuple
import matplotlib.pyplot as plt
import tensorflow as tf


def plot_everything(history1: tf.keras.callbacks.History, history2: tf.keras.callbacks.History,
                    para_list1: List[Tuple[str, str, str]], para_list2: List[Tuple[str, str, str]]) -> None:
    """
    Display, on a window,
    the progression of loss over the course of training for the two models/neural networks,
    and the final best-performing parameters for maximum peak interest or interest longevity.

    Preconditions:
        - para_list1 != []
        - para_list2 != []
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
    fig.suptitle('Results: Model training losses and final best parameters', fontsize=14, fontweight='bold')

    ax1.set_title('Peak interest model')
    ax2.set_title('Longevity interest model')

    ax1.plot(history1.history['loss'])
    ax2.plot(history2.history['loss'])

    ax1.set_ylim([0, 70])
    ax2.set_ylim([0, 1.1])

    ax1.grid(True)
    ax1.set_xlabel('epochs')
    ax1.set_ylabel('MAE loss')

    ax2.grid(True)
    ax2.set_xlabel('epochs')
    ax2.set_ylabel('MAE loss')

    fig.tight_layout()

    peak_best = _pick_parameters_for_display(para_list1)
    longevity_best = _pick_parameters_for_display(para_list2)

    textstr1 = 'best parameters for max. $\\bf{PEAK}$ interest: ' + peak_best[1] + ' in ' + peak_best[2] + ' during ' + peak_best[0] + '\n'
    textstr2 = 'best parameters for max. interest $\\bf{LONGEVITY}$: ' + longevity_best[1] + ' in ' + longevity_best[2] + ' during ' + \
               longevity_best[0]

    fig.text(0.02, 0.05, textstr1 + textstr2, fontsize=12, wrap=True)
    plt.subplots_adjust(bottom=0.3)

    plt.show()


def _pick_parameters_for_display(para_list: List[Tuple[str, str, str]]) -> Tuple[str, str, str]:
    """
    From the list of best performing set of parameters returned from find_parameters.find_best_parameters(),
    find the most-occurring parameter set,
    i.e. the single set of parameters which yields maximum peak or longevity values for
        the majority of death-affected scenarios.

    Preconditions:
        - para_list != []

    >>> _pick_parameters_for_display([('a', 'b', 'c'), ('a', 'b', 'c'), ('c', 'd', 'e')])
    ('a', 'b', 'c')
    """
    best = para_list[0]
    counter = 0

    for element in para_list:
        freq = para_list.count(element)
        if freq > counter:
            counter = freq
            best = element

    return best


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports':
            ['python_ta.contracts', 'matplotlib.pyplot', 'tensorflow'],
        'max-line-length': 200,
        'allowed-io': [],
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)
