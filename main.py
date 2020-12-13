import model as pm

if __name__ == '__main__':
    model_a = pm.Model('peak')
    model_b = pm.Model('longevity')

    model_a.train()
    model_a.test()

    model_b.train()
    model_b.test()

