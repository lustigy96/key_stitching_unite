import numpy as np
import pandas as pd
import key_stitching_functinos as func
from key_stitching_functinos import build_samples_continues
import os
import matplotlib.pyplot as plt
from bitstring import BitArray




def Compute_precitle_of_good_samples(allGoodPossible, percentileArray, expNum, max, min, goodDidntShow, rezolution):
    """
    this function computes for specific experiment in which precitles and how many good samples are
    :param allGoodPossible: dict of good sample and its count {"1010100..": count}
    :param result_df:
    :param percentileArray:
    :param expNum:
    """
    onePrecentile = (max-min) / rezolution

    for goodSample in allGoodPossible.keys():
        if allGoodPossible[goodSample]["count"] == 0:
            goodDidntShow[expNum] += 1
        else:
            for i in range(1, rezolution):
                if allGoodPossible[goodSample]["count"] > (i-1)*onePrecentile and  allGoodPossible[goodSample]["count"] <= i*onePrecentile:
                    percentileArray[i-1][expNum] += 1
            if allGoodPossible[goodSample]["count"] > (rezolution-1)*onePrecentile:
                percentileArray[rezolution-1][expNum] += 1

    return percentileArray








def Compute_statistics_for_spesific_error_type(type, numberOfExpiriments, key, fragment_len, fragments_number, window_size, allGoodPossible_dict, rezolution ):
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
    CDFArray = np.zeros(numberOfExpiriments, dtype=np.float64)
    meanArray = np.zeros(numberOfExpiriments, dtype=np.float64)
    varianceArray = np.zeros(numberOfExpiriments, dtype=np.float64)
    maxArray = np.zeros(numberOfExpiriments, dtype=np.int)
    minArray = np.zeros(numberOfExpiriments, dtype=np.int)
    goodDidntShow = np.zeros(numberOfExpiriments, dtype=np.int)
    percentileArray = np.zeros([rezolution, numberOfExpiriments], dtype=np.uint32)

    error =  error_dict[type]
    for expNum in xrange(0,numberOfExpiriments):
        result_df, result_dict, allGoodPossible_df, allGoodPossible_dict = \
            func.build_samples_continues_with_statistics_of_good(key=key, sample_begin=0, sample_end=fragments_number, fragment_len=fragment_len,
                                                                 window_size=window_size, flip_probability=error["f"], delete_probability=error["d"],
                                                                 insert_probability=error["i"], result_dict={}, allGoodPossible_dict=allGoodPossible_dict)

        result_df = result_df.sort_values('count', ascending=False).reset_index()
        allGoodPossible_df = allGoodPossible_df.sort_values('count', ascending=False).reset_index()
        idxmin = allGoodPossible_df['count'].idxmin()

        last_index__of_good_window  = result_df.loc[0]
        for index in result_df.index:
            CDFArray[expNum] = 1

        meanArray[expNum] = result_df["count"].mean()
        varianceArray[expNum] = result_df["count"].var()
        maxArray[expNum] = result_df["count"].max()
        minArray[expNum] = result_df["count"].min()
        percentileArray = Compute_precitle_of_good_samples(allGoodPossible=allGoodPossible_dict,
                                                           percentileArray=percentileArray,
                                                           expNum=expNum,
                                                           max=maxArray[expNum],
                                                           min=minArray[expNum],
                                                           goodDidntShow=goodDidntShow,
                                                           rezolution=rezolution)
    percentile = np.zeros(rezolution, dtype=np.float64)
    for i in range(0, rezolution):
        percentile[i] = percentileArray[i].mean()


    mean = meanArray.mean()
    variance = varianceArray.mean()
    max = maxArray.mean()
    min = minArray.mean()
    result = {"mean":mean ,
              "variance":variance,
              "percentile":percentile,
              'goodDidntShowed':goodDidntShow.mean(),
              'max':max,
              'min': min}
    return result



def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')




if __name__ == "__main__":

    error_dict = {
        "mixed": {"f": 0.03, "d": 0.03, "i": 0.03},
        "onlyFips": {"f": 0.09, "d": 0.0, "i": 0.0},
        "onlyDeletions": {"f": 0.0, "d": 0.09, "i": 0.0},
        "onlyInsertions": {"f": 0.0, "d": 0.0, "i": 0.09}
    }

    hex_key_2048 = "40554dc4edd210b27e4be5d4d6dcde0f3ab8199730db8a5cf3f3d1617d956cd7dfa0b1e7f82f0b0949d67f7b2b3f84e62537d41eb0142aaf1f84aa6d74b1e0aa2bf82f84298e6d9f6aa580c75905bda8508aad6b73f75862246a7aebe964d543fa05b455b58a3a0f301ab9d9f4232a82e5aaed1303514109f0b4526eb5706c1d3c231e9bd9c96f647774fc923686f17b8707035db6b3f16163154c1d11276540ec776b341fe292def59bcfe161869fae2dc04de17603ae012a3b22d611a3643414e7eff365c8bd3b35323f56759dc6a9dd7704f5d760deb29e8bbd50586b8df7ee9c33d6b6abf9b625635b9db15360c5eae2b89dc4ff443722e5e6b06f71e930"
    key = key2048 = ''.join(func.hex2bin_map[i] for i in hex_key_2048)
    key_length = len(key)
    fragment_len = 23
    fragments_number = 100
    window_size = 22
    numberOfExpiriments = 1
    rezolution = 25
    resultDict = {
        "onlyFips": None,
        # "onlyDeletions": None,
        # "onlyInsertions": None,
        "mixed": None
    }

    allGoodPossible_dict = func.All_possible_window_good_strings(key=key, window_size=window_size)

    for i, type in enumerate(resultDict.keys(), 0):
        result =  Compute_statistics_for_spesific_error_type(type=type, numberOfExpiriments=numberOfExpiriments, key=key,
                                                             fragment_len=fragment_len, fragments_number=fragments_number,
                                                             window_size=window_size, allGoodPossible_dict=allGoodPossible_dict,
                                                             rezolution=rezolution)
        resultDict[type] = result
        for goodSample in allGoodPossible_dict.keys():
            allGoodPossible_dict[goodSample]["count"] = 0

    #print
    for type in resultDict.keys():
        print type
        print 'max: ' + str(resultDict[type]['max'])
        print 'min: ' + str(resultDict[type]['min'])
        print 'goodDidntShowed: ' + str(resultDict[type]['goodDidntShowed'])

    labelsF = []
    pixel = 100/rezolution
    for i in range(0,rezolution):
        labelsF.append('({0}-{1})%'.format(i*pixel,(i+1)*pixel))

    x = np.arange(len(labelsF))  # the label locations
    widthBar = 0.40  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - widthBar/2, resultDict['onlyFips']['percentile'], widthBar/4, label='onlyFips')
    # rects2 = ax.bar(x - widthBar/4, resultDict['onlyDeletions']['percentile'], widthBar/4, label='onlyDeletions')
    # rects3 = ax.bar(x + widthBar/4, resultDict['onlyInsertions']['percentile'], widthBar/4, label='onlyInsertions')
    rects4 = ax.bar(x + widthBar/2, resultDict['mixed']['percentile'], widthBar/4, label='mixed')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Number of good strings')
    ax.set_title('percentile of good strings')
    ax.set_xticks(x)
    ax.set_xticklabels(labelsF)
    ax.legend()
    autolabel(rects1)
    # autolabel(rects2)
    # autolabel(rects3)
    autolabel(rects4)
    fig.tight_layout()
    # plt.show()


    labelsF = ['mean']
    x = np.arange(len(labelsF))  # the label locations
    widthBar = 0.40  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - widthBar/2, resultDict['onlyFips']['mean'], widthBar/4, label='onlyFips')
    # rects2 = ax.bar(x - widthBar/4, resultDict['onlyDeletions']['mean'], widthBar/4, label='onlyDeletions')
    # rects3 = ax.bar(x + widthBar/4, resultDict['onlyInsertions']['mean'], widthBar/4, label='onlyInsertions')
    rects4 = ax.bar(x + widthBar/2, resultDict['mixed']['mean'], widthBar/4, label='mixed')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('the mean value')
    ax.set_title('the mean value of strings')
    ax.set_xticks(x)
    ax.set_xticklabels(labelsF)
    ax.legend()
    autolabel(rects1)
    # autolabel(rects2)
    # autolabel(rects3)
    autolabel(rects4)
    fig.tight_layout()




    labelsF = ['variance']
    x = np.arange(len(labelsF))  # the label locations
    widthBar = 0.40  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - widthBar/2, resultDict['onlyFips']['variance'], widthBar/4, label='onlyFips')
    # rects2 = ax.bar(x - widthBar/4, resultDict['onlyDeletions']['variance'], widthBar/4, label='onlyDeletions')
    # rects3 = ax.bar(x + widthBar/4, resultDict['onlyInsertions']['variance'], widthBar/4, label='onlyInsertions')
    rects4 = ax.bar(x + widthBar/2, resultDict['mixed']['variance'], widthBar/4, label='mixed')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('variance value')
    ax.set_title('the variance value of all strings')
    ax.set_xticks(x)
    ax.set_xticklabels(labelsF)
    ax.legend()
    autolabel(rects1)
    # autolabel(rects2)
    # autolabel(rects3)
    autolabel(rects4)
    fig.tight_layout()


    plt.show()






















