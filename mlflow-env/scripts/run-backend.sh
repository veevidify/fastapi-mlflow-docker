#!/bin/bash

# run a Tracking backend API listening on 5000
# and using postgres (dockerised locally) as registry
mlflow server --backend-store-uri postgresql://postgres:123456@localhost/app \
                --default-artifact-root file:./artifacts \
                --host 0.0.0.0 \
                --port 5000 &
