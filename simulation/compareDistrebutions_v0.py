import numpy as np
import pandas as pd
import key_stitching_functinos as func
from key_stitching_functinos import build_samples_continues
import os
import matplotlib.pyplot as plt
from bitstring import BitArray


error_dict = {
    "mixed": {"f": 0.05,
              "d": 0.05,
              "i": 0.05,
              },
    "onlyFips": {"f": 0.15,
                 "d": 0.0,
                 "i": 0.0,
                 },
    "onlyDeletions": {"f": 0.0,
                  "d": 0.15,
                  "i": 0.0,
                  },
    "onlyInsertions": {"f": 0.0,
                  "d": 0.0,
                  "i": 0.15,
                  }

}


key = func.init_key(2048, -1)
key_length = len(key)
key = func.init_key(key_length, -1)
fragment_len = 23
samples_number = 700000
window_size = 22

result_df = {"onlyFips":None, "mixed": None}
# fig, axes = plt.subplots(nrows=2, ncols=2)

all2PowerWindowArray1 = np.zeros(2 ** window_size, dtype=np.float64)
all2PowerWindowArray2 = np.zeros(2 ** window_size, dtype=np.float64)
all2PowerWindowArray3 = np.zeros(2 ** window_size, dtype=np.float64)
all2PowerWindowArray4 = np.zeros(2 ** window_size, dtype=np.float64)


for i, type in enumerate(result_df.keys(), 0):
    fig, ax = plt.subplots()

    error =  error_dict[type]
    result_df[type], result_dict = build_samples_continues(key=key, sample_begin=0, sample_end=samples_number,
                                                          sample_len=fragment_len, window_size=window_size,
                                                          flip_probability=error["f"], delete_probability=error["d"], insert_probability=error["i"],
                                                          result_dict={})
    result_df[type] = result_df[type].sort_values('count', ascending=False)
    # TotalSum = result_df[type]['count'].sum()
    # result_df[type]['count'] = result_df[type]['count']/ TotalSum


    n_rows = result_df[type].shape[0]
    x = range(0, n_rows)
    y = result_df[type]["count"]
    ax.set_title(type + " Error - Histogram")
    ax.set_ylabel("Number Of Strings")

    ax.plot(x, y, marker='o', linewidth=2, markersize=1)
    ax.grid()


plt.show()