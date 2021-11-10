#!/bin/bash

curl --request POST http://0.0.0.0:8003/invocations \
       --header "Content-Type:application/json; format=pandas-split" \
       --data '{
    "columns":["age", "sex", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6"],
    "data":[[0.01628, -0.04464, 0.00133, 0.00810, 0.00531, 0.01089, 0.03023, -0.03949, -0.04542, 0.03205]]
  }'
