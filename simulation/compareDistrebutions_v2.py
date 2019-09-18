import numpy as np
import pandas as pd
import key_stitching_functinos as func
from key_stitching_functinos import build_samples_continues
import os
import matplotlib.pyplot as plt
from bitstring import BitArray










def Compute_statistics_for_spesific_error_type(type, numberOfExpiriments, key, fragment_len, fragments_number, window_size, allGoodPossible_dict):
    """this function genertes several expiriments of given error type in order to collect some statistcs
    of the such error: mean value, variance etc ..
    """
    CDFArrayOffAllGood = np.zeros(numberOfExpiriments, dtype=np.uint64)
    CDFArrayOffAllBadsInAllGoods = np.zeros(numberOfExpiriments, dtype=np.uint64)
    CDFArrayOffAll = np.zeros(numberOfExpiriments, dtype=np.uint64)
    meanArray = np.zeros(numberOfExpiriments, dtype=np.float64)
    varianceArray = np.zeros(numberOfExpiriments, dtype=np.float64)
    maxArray = np.zeros(numberOfExpiriments, dtype=np.int)
    minArray = np.zeros(numberOfExpiriments, dtype=np.int)
    goodDidntShow = np.zeros(numberOfExpiriments, dtype=np.int)

    error =  error_dict[type]
    for expNum in xrange(0,numberOfExpiriments):
        result_df, result_dict, allGoodPossible_df, allGoodPossible_dict = \
            func.build_samples_continues_with_statistics_of_good(key=key, sample_begin=0, sample_end=fragments_number, fragment_len=fragment_len,
                                                                 window_size=window_size, flip_probability=error["f"], delete_probability=error["d"],
                                                                 insert_probability=error["i"], result_dict={}, allGoodPossible_dict=allGoodPossible_dict)

        result_df = result_df.sort_values('count', ascending=False).reset_index() # sort and add indexes
        allGoodPossible_df = allGoodPossible_df.sort_values('count', ascending=False).reset_index() # sort and add indexes
        idxmin = allGoodPossible_df['count'].idxmin()
        # min_good_sample = allGoodPossible_df['sample'].loc[idxmin]
        last_index_of_good_window = -1
        for index in result_df.index:
            if result_df['sample'].loc[index] in allGoodPossible_dict: #we found the index of the last good sample in all data frame
                last_index_of_good_window = index


        CDFArrayOffAll[expNum] = result_df['count'].sum()
        CDFArrayOffAllGood[expNum] =  allGoodPossible_df['count'].sum()
        CDFArrayOffAllBadsInAllGoods[expNum] = result_df['count'].loc[0:last_index_of_good_window].sum()

        meanArray[expNum] = result_df["count"].mean()
        varianceArray[expNum] = result_df["count"].var()
        maxArray[expNum] = result_df["count"].max()
        minArray[expNum] = result_df["count"].min()

        #compute how many good samples didnt exsist at all in thw whole data
        goodDidntShow[expNum] = len(allGoodPossible_df[allGoodPossible_df['count']==0])




    mean = meanArray.mean()
    variance = varianceArray.mean()
    max = maxArray.mean()
    min = minArray.mean()
    result = {"mean":mean ,
              "variance":variance,
              'goodDidntShowed':goodDidntShow.mean(),
              'CDFArrayOffAll' : CDFArrayOffAll.mean(),
              'CDFArrayOffAllGood' : CDFArrayOffAllGood.mean(),
              'CDFArrayOffAllBadsInAllGoods' : CDFArrayOffAllBadsInAllGoods.mean(),
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
                                                             )
        resultDict[type] = result
        for goodSample in allGoodPossible_dict.keys():
            allGoodPossible_dict[goodSample]["count"] = 0

    #print
    #print
    for type in resultDict.keys():
        print type
        print 'max: ' + str(resultDict[type]['max'])
        print 'min: ' + str(resultDict[type]['min'])
        print 'goodDidntShowed: ' + str(resultDict[type]['goodDidntShowed'])
        print "\n"


    labelsF = ['CDFArrayOffAll', 'CDFArrayOffAllGood', 'CDFArrayOffAllBadsInAllGoods']
    x = np.arange(len(labelsF))  # the label locations
    for type in resultDict.keys():
        widthBar = 0.40  # the width of the bars
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - widthBar, resultDict[type]['CDFArrayOffAll'], widthBar, label='CDFArrayOffAll')
        rects2 = ax.bar(x, resultDict[type]['CDFArrayOffAllGood'], widthBar, label='CDFArrayOffAllGood')
        rects3 = ax.bar(x + widthBar, resultDict[type]['CDFArrayOffAllBadsInAllGoods'], widthBar, label='CDFArrayOffAllBadsInAllGoods')
        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Number of strings')
        ax.set_title('{0} - cdf statistics of good strings vs bad'.format(type))
        ax.set_xticks(x)
        ax.set_xticklabels(labelsF)
        ax.legend()
        autolabel(rects1)
        autolabel(rects2)
        autolabel(rects3)
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




















