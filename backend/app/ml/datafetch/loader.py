import pandas as pd
import numpy as np

from sklearn import datasets

def load_dataset():
    # Load Diabetes datasets
    diabetes = datasets.load_diabetes()
    X = diabetes.data
    y = diabetes.target

    # Create pandas DataFrame for sklearn ElasticNet linear_model
    Y = np.array([y]).transpose()
    d = np.concatenate((X, Y), axis=1)
    cols = diabetes.feature_names + ["progression"]
    data = pd.DataFrame(d, columns=cols)

    return data, X, y
