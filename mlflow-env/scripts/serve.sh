#!/bin/bash

# serve will create a conda env to run the model code,
# mlflow-wrapped, allowing to call train/predict via /invocations REST api
mlflow models serve \
-m file:./artifacts/0/a45e2c93ae95413594f06af35aa3e53a/artifacts/model \
-h 0.0.0.0 \
-p 8003
