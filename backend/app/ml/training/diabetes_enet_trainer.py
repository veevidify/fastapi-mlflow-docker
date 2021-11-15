import os
import warnings
import sys

import numpy as np
import matplotlib.pyplot as plt

from itertools import cycle
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import lasso_path, enet_path

from ml.datafetch.loader import load_dataset

# Import mlflow
import mlflow
import mlflow.sklearn

#   MLflow model using ElasticNet (sklearn) and Plots ElasticNet Descent Paths
#
#   Uses the sklearn Diabetes dataset to predict diabetes progression using ElasticNet
#       The predicted "progression" column is a quantitative measure of disease progression one year after baseline
#       http://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_diabetes.html
#   Combines the above with the Lasso Coordinate Descent Path Plot
#       http://scikit-learn.org/stable/auto_examples/linear_model/plot_lasso_coordinate_descent_path.html
#       Original author: Alexandre Gramfort <alexandre.gramfort@inria.fr>; License: BSD 3 clause
#
#  Usage:
#    python diabetes_enet_trainer.py 0.01 0.01
#    python diabetes_enet_trainer.py 0.01 0.75
#    python diabetes_enet_trainer.py 0.01 1.0

# Evaluate metrics
def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

def mlflow_logging(model, params: dict, metrics: dict):
    for k in params:
        v = params[k]
        mlflow.log_param(k, v)

    for k in metrics:
        v = metrics[k]
        mlflow.log_metric(k, v)

    mlflow.sklearn.log_model(model, "model")

def construct_persist_fig(X, y, alpha: float, l1_ratio: float):
    # Compute paths
    eps = 5e-3  # the smaller it is the longer is the path

    print("Computing regularization path for figure using trained model.")
    # alphas_enet, coefs_enet, _ = enet_path(X, y, eps=eps, l1_ratio=l1_ratio, fit_intercept=False)
    alphas_enet, coefs_enet, _ = enet_path(X, y, eps=eps, l1_ratio=l1_ratio)

    # Construct figs to display results
    fig = plt.figure(1)
    ax = plt.gca()

    colors = cycle(["b", "r", "g", "c", "k"])
    neg_log_alphas_enet = -np.log10(alphas_enet)
    for coef_e, c in zip(coefs_enet, colors):
        l2 = plt.plot(neg_log_alphas_enet, coef_e, linestyle="--", c=c)

    plt.xlabel("-Log(alpha)")
    plt.ylabel("coefficients")
    title = "ElasticNet Path by alpha for l1_ratio = " + str(l1_ratio)
    plt.title(title)
    plt.axis("tight")

    # Save figures
    fig.savefig("temp/ElasticNet-paths.png")

    # Close plot
    plt.close(fig)

    # Log artifacts (output files)
    mlflow.log_artifact("temp/ElasticNet-paths.png")
    mlflow.log_artifact('temp/diabetes.txt')

# alpha & l1 will be passed by caller - api or console
def train_enet_diabetes_dataset(alpha: float, l1_ratio: float):
    warnings.filterwarnings("ignore")
    np.random.seed(40)

    # prepare dataset
    data, X, y = load_dataset()

    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "progression" which is a quantitative measure of disease progression one year after baseline
    train_x = train.drop(["progression"], axis=1)
    test_x = test.drop(["progression"], axis=1)
    train_y = train[["progression"]]
    test_y = test[["progression"]]

    run_id = None
    with mlflow.start_run() as run:
        # print(mlflow.get_tracking_uri())
        # print(mlflow.get_artifact_uri())

        # ElasticNet Fit-Predict
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)
        predicted_qualities = lr.predict(test_x)
        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

        # Console logging ElasticNet model metrics
        print("Elasticnet model with (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        # mlflow logging attributes for mlflow UI
        params_dict = {
            "alpha": alpha,
            "l1_ratio": l1_ratio,
        }
        metrics_dict = {
            "rmse": rmse,
            "r2": r2,
            "mae": mae,
        }

        mlflow_logging(lr, params_dict, metrics_dict)

        # persist training data
        data.to_csv('temp/diabetes.txt', encoding="utf-8", index=False)

        construct_persist_fig(X, y, alpha, l1_ratio)

        print("Active run: {}".format(run.info.run_id))
        run_id = run.info.run_id

    return run_id

# for test model directly from console poetry venv
if __name__ == "__main__":
    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.05
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05

    # from within the container (if desire),
    # this uri has to be http://mlflow:MLFLOW_PORT ?
    mlflow.set_tracking_uri('http://localhost:5005')
    train_enet_diabetes_dataset(alpha, l1_ratio)
