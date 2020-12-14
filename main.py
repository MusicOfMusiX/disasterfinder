"""
CSC110 Fall 2020 Project - main.py

OBJECTIVE: Find the optimum season, disaster type, and region for a natural disaster to
            yield maximum Google search interest peaks and longevity.

This file is Copyright (c) 2020 Hyun Jo (Joshua) Jang.
"""

import model
import find_parameters
import process_results

if __name__ == '__main__':
    # Build and train NN model for peak interest
    model_a = model.Model('peak')
    model_a_log = model_a.train()
    # model_a.test()  # Uncomment to see test results

    # Build and train NN model for longevous/longevity interest
    model_b = model.Model('longevity')
    model_b_log = model_b.train()
    # model_b.test()  # Uncomment to see test results

    # Find best parameters for both categories
    best_peak_parameters = find_parameters.find_best_parameters(model_a)
    best_longevity_parameters = find_parameters.find_best_parameters(model_b)

    # Plot results: model loss history and best parameters
    process_results.plot_everything(model_a_log, model_b_log, best_peak_parameters, best_longevity_parameters)
