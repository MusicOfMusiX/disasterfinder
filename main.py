import model
import find_parameters
import process_results

if __name__ == '__main__':
    model_a = model.Model('peak')
    model_a_log = model_a.train()

    model_b = model.Model('longevity')
    model_b_log = model_b.train()

    best_peak_parameters = find_parameters.find_best_parameters(model_a)
    best_longevity_parameters = find_parameters.find_best_parameters(model_b)

    #process_results.XXX(model_a_log, model_b_log, best_peak_parameters, best_longevity_parameters)
    process_results.plot_loss(model_a_log, model_b_log)
