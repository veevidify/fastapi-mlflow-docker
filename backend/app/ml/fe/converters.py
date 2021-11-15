from typing import List

import json
import numpy as np

from app import schemas

def convert_dict_datapoints(datapoints: List[schemas.DatapointToPredict]):
    # return np array collection of datapoints,
    # assuming converted to numbers (feature extracted & scaled)

    inputs = None
    for dp in datapoints:
        keys = ["age", "sex", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6"]
        dp_dict = json.loads(dp.json())
        entry = np.array([dp_dict[key] for key in keys])

        # tricks
        if (inputs is None):
            inputs = [entry]
        else:
            inputs = np.vstack([inputs, entry])

    return inputs
