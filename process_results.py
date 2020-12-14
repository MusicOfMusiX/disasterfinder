import matplotlib.pyplot as plt
from typing import List, Tuple


def plot_everything(history1, history2, para_list1: List[Tuple[str, str, str]], para_list2: List[Tuple[str, str, str]]):

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
    textstr2 = 'best parameters for max. $\\bf{LONGEVITY}$ interest: ' + longevity_best[1] + ' in ' + longevity_best[2] + ' during ' + \
               longevity_best[0]

    fig.text(0.02, 0.05, textstr1 + textstr2, fontsize=12, wrap=True)
    plt.subplots_adjust(bottom=0.3)

    plt.show()


def _pick_parameters_for_display(para_list: List[Tuple[str, str, str]]):
    best = para_list[0]
    counter = 0

    for element in para_list:
        freq = para_list.count(element)
        if freq > counter:
            counter = freq
            best = element

    return best

