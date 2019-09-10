import numpy as np
import pandas as pd
import key_stitching_functinos as func
from key_stitching_functinos import build_samples_continues
import os
# import matplotlib.pyplot as plt
from bitstring import BitArray




def Compute_precitle_of_good_samples(allGoodPossible, result_df, percentileArray, expNum):
    """
    this function computes for specific experiment in which precitles and how many good samples are
    :param allGoodPossible: dict of good sample and its count {"1010100..": count}
    :param result_df:
    :param percentileArray:
    :param expNum:
    """
    max = result_df["count"].max()
    precentile10 = max / 10
    for goodSample in allGoodPossible.keys():
        if allGoodPossible[goodSample]["count"] <= 1*precentile10:
            percentileArray["0-10"][expNum] += 1
        elif allGoodPossible[goodSample]["count"] > 1*precentile10 and allGoodPossible[goodSample]["count"] <= 2*precentile10:
            percentileArray["10-20"][expNum] += 1
        elif allGoodPossible[goodSample]["count"] > 2*precentile10 and allGoodPossible[goodSample]["count"] <= 3*precentile10:
            percentileArray["20-30"][expNum] += 1
        elif allGoodPossible[goodSample]["count"] > 3*precentile10 and allGoodPossible[goodSample]["count"] <= 4*precentile10:
            percentileArray["30-40"][expNum] += 1
        elif allGoodPossible[goodSample]["count"] > 4*precentile10 and allGoodPossible[goodSample]["count"] <= 5*precentile10:
            percentileArray["40-50"][expNum] += 1
        elif allGoodPossible[goodSample]["count"] > 5*precentile10 and allGoodPossible[goodSample]["count"] <= 6*precentile10:
            percentileArray["50-60"][expNum] += 1
        elif allGoodPossible[goodSample]["count"] > 6*precentile10 and allGoodPossible[goodSample]["count"] <= 7*precentile10:
            percentileArray["60-70"][expNum] += 1
        elif allGoodPossible[goodSample]["count"] > 7*precentile10 and allGoodPossible[goodSample]["count"] <= 8*precentile10:
            percentileArray["70-80"][expNum] += 1
        elif allGoodPossible[goodSample]["count"] > 8*precentile10 and allGoodPossible[goodSample]["count"] <= 9*precentile10:
            percentileArray["80-90"][expNum] += 1
        elif allGoodPossible[goodSample]["count"] > 9*precentile10:
            percentileArray["90-100"][expNum] += 1

def Compute_statistics_for_spesific_error_type(type, numberOfExpiriments, key, fragment_len, fragments_number, window_size, allGoodPossible ):
    """this function genertes several expiriments of given error type in order to collect some statistcs
    of the such error: mean value, variance etc ..

    :param type: which type of error this function would test ("onlyFips", "onlyDeletions", "onlyInsertions", "mixed")
    :param numberOfExpiriments: how much expiriments run this test
    :param key: random key
    :param fragment_len: the length of single fragment
    :param fragments_number: number of framgents
    :param window_size: the window size for the sfs algorithem
    :rtype: dict
    :return: "mean", "variance"
    """
    meanArray = np.zeros(numberOfExpiriments, dtype=np.float64)
    varianceArray = np.zeros(numberOfExpiriments, dtype=np.float64)
    percentileArray = {}
    percentile = {}
    percentileArray["0-10"] = np.zeros(numberOfExpiriments, dtype=np.uint32)
    percentile["0-10"] = 0
    percentileArray["10-20"] = np.zeros(numberOfExpiriments, dtype=np.uint32)
    percentile["10-20"] = 0
    percentileArray["20-30"] = np.zeros(numberOfExpiriments, dtype=np.uint32)
    percentile["20-30"] = 0
    percentileArray["30-40"] = np.zeros(numberOfExpiriments, dtype=np.uint32)
    percentile["30-40"] = 0
    percentileArray["40-50"] = np.zeros(numberOfExpiriments, dtype=np.uint32)
    percentile["40-50"] = 0
    percentileArray["50-60"] = np.zeros(numberOfExpiriments, dtype=np.uint32)
    percentile["50-60"] = 0
    percentileArray["60-70"] = np.zeros(numberOfExpiriments, dtype=np.uint32)
    percentile["60-70"] = 0
    percentileArray["70-80"] = np.zeros(numberOfExpiriments, dtype=np.uint32)
    percentile["70-80"] = 0
    percentileArray["80-90"] = np.zeros(numberOfExpiriments, dtype=np.uint32)
    percentile["80-90"] = 0
    percentileArray["90-100"] = np.zeros(numberOfExpiriments, dtype=np.uint32)
    percentile["90-100"] = 0

    error =  error_dict[type]
    for expNum in xrange(0,numberOfExpiriments):
        result_df, result_dict, allGoodPossible = \
            func.build_samples_continues_with_statistics_of_good(key=key, sample_begin=0, sample_end=fragments_number, fragment_len=fragment_len,
                                    window_size=window_size, flip_probability=error["f"], delete_probability=error["d"],
                                    insert_probability=error["i"], result_dict={}, allGoodPossible=allGoodPossible)
        meanArray[expNum] = result_df["count"].mean()
        varianceArray[expNum] = result_df["count"].var()
        percentileArray = Compute_precitle_of_good_samples(allGoodPossible=allGoodPossible, result_df=result_df,
                                                          percentileArray=percentileArray, expNum=expNum)
    for dkey in percentileArray.keys():
        percentile[dkey] = percentileArray[dkey].mean()

    mean = meanArray.mean()
    variance = varianceArray.mean()
    result = {"mean":mean , "variance":variance,"percentile":percentile}
    return result





if __name__ == "__main__":

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

    hex_key_2048 = "40554dc4edd210b27e4be5d4d6dcde0f3ab8199730db8a5cf3f3d1617d956cd7dfa0b1e7f82f0b0949d67f7b2b3f84e62537d41eb0142aaf1f84aa6d74b1e0aa2bf82f84298e6d9f6aa580c75905bda8508aad6b73f75862246a7aebe964d543fa05b455b58a3a0f301ab9d9f4232a82e5aaed1303514109f0b4526eb5706c1d3c231e9bd9c96f647774fc923686f17b8707035db6b3f16163154c1d11276540ec776b341fe292def59bcfe161869fae2dc04de17603ae012a3b22d611a3643414e7eff365c8bd3b35323f56759dc6a9dd7704f5d760deb29e8bbd50586b8df7ee9c33d6b6abf9b625635b9db15360c5eae2b89dc4ff443722e5e6b06f71e930"
    key = key2048 = ''.join(func.hex2bin_map[i] for i in hex_key_2048)
    key_length = len(key)
    fragment_len = 40
    fragments_number = 2000
    window_size = 22
    numberOfExpiriments = 1

    resultDict = {"onlyFips": None, "onlyDeletions": None, "onlyInsertions": None, "mixed": None}

    # fig, axes = plt.subplots(nrows=2, ncols=2)

    subp = {
        0: {"r": 0, "c": 0},
        1: {"r": 0, "c": 1},
        2: {"r": 1, "c": 0},
        3: {"r": 1, "c": 1},
    }

    allGoodPossible = func.All_possible_window_strings(key=key, window_size=window_size)

    for i, type in enumerate(resultDict.keys(), 0):
        result =  Compute_statistics_for_spesific_error_type(type=type, numberOfExpiriments=numberOfExpiriments, key=key,
                                                             fragment_len=fragment_len, fragments_number=fragments_number,
                                                             window_size=window_size, allGoodPossible=allGoodPossible)
        resultDict[type] = result



        # TotalSum = result_df[type]['count'].sum()
        # result_df[type]['count'] = result_df[type]['count']/ TotalSum


        # n_rows = result_df[type].shape[0]
        # x = range(0, n_rows)
        # y = result_df[type]["count"]
        # axes[subp[i]["r"], subp[i]["c"]].set_title(type + " errors")
        # axes[subp[i]["r"], subp[i]["c"]].plot(x, y, marker='o', linewidth=1, markersize=1)
        # axes[subp[i]["r"], subp[i]["c"]].grid()
    #
    #
    # plt.show()





