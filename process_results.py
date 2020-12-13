import matplotlib.pyplot as plt
from typing import List, Tuple


def plot_loss(history1, history2):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('MAE loss history for peak and longevity models')

    ax1.plot(history1.history['loss'])
    ax2.plot(history2.history['loss'])

    ax1.set_ylim([0, 70])
    ax2.set_ylim([0, 1.35])

    ax1.legend()
    ax1.grid(True)
    ax1.set_xlabel('epochs')
    ax1.set_ylabel('loss')

    ax2.legend()
    ax2.grid(True)
    ax2.set_xlabel('epochs')
    ax2.set_ylabel('loss')

    plt.show()


def _pick_parameters_for_display(para_list1: List[Tuple[str, str, str]], para_list2: List[Tuple[str, str, str]]):
    pass
