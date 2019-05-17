#! /usr/bin/python

import xlsxwriter
import yaml

import numpy as np
import pandas as pd
import logging

import threading
import time
# import matplotlib.pyplot as plt
import os
import operator as op
from functools import reduce
from bitstring import BitArray
import sys
import key_stitching_functinos as func



if __name__ == "__main__":
    SIMULATION = False
    REAL = True
    # DATA_FILE_PATH = "./results/simulation/table.txt"
    # with open(DATA_FILE_PATH, "r") as dataFile:
    #     str = dataFile.read()
    #
    # tableDictResult = yaml.load(str)
    # print tableDictResult


    if SIMULATION:
        tableResult = {'key_length512': {'sample_len31': {'window_size20': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 471, 'D': 471, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 469, 'D': 469, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 464, 'D': 464, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 461, 'D': 461, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 465, 'D': 465, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 453, 'D': 453, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 43, 'DIST': 43, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 66, 'DIST': 66, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 364, 'D': 364, 'F': 0}, 'samples_num3000000': {'I': 47, 'DIST': 47, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 35, 'DIST': 35, 'D': 0, 'F': 0}, 'samples_num1000000': {'I': 48, 'DIST': 48, 'D': 0, 'F': 0}}, 'error5': {'samples_num4000000': {'I': 29, 'DIST': 29, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 24, 'DIST': 24, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 12, 'DIST': 12, 'D': 0, 'F': 0}, 'samples_num3000000': {'I': 29, 'DIST': 29, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 28, 'DIST': 28, 'D': 0, 'F': 0}, 'samples_num1000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}}, 'error7': {'samples_num4000000': {'I': 38, 'DIST': 38, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 18, 'DIST': 18, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 15, 'DIST': 15, 'D': 0, 'F': 0}, 'samples_num3000000': {'I': 31, 'DIST': 31, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 28, 'DIST': 28, 'D': 0, 'F': 0}, 'samples_num1000000': {'I': 13, 'DIST': 14, 'D': 0, 'F': 1}}}, 'window_size30': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 477, 'D': 477, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 474, 'D': 474, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 475, 'D': 475, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 476, 'D': 476, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 476, 'D': 476, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 477, 'D': 477, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 0, 'DIST': 442, 'D': 442, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 478, 'D': 478, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 480, 'D': 480, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 448, 'D': 448, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 461, 'D': 461, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 474, 'D': 474, 'F': 0}}, 'error5': {'samples_num4000000': {'I': 4, 'DIST': 4, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 1, 'DIST': 1, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 387, 'D': 387, 'F': 0}, 'samples_num3000000': {'I': 3, 'DIST': 4, 'D': 0, 'F': 1}, 'samples_num2000000': {'I': 3, 'DIST': 3, 'D': 0, 'F': 0}, 'samples_num1000000': {'I': 2, 'DIST': 2, 'D': 0, 'F': 0}}, 'error7': {'samples_num4000000': {'I': 3, 'DIST': 3, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 410, 'D': 410, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 474, 'D': 474, 'F': 0}, 'samples_num3000000': {'I': 3, 'DIST': 4, 'D': 0, 'F': 1}, 'samples_num2000000': {'I': 2, 'DIST': 3, 'D': 1, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 258, 'D': 258, 'F': 0}}}}, 'sample_len100': {'window_size20': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 362, 'D': 362, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 386, 'D': 386, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 355, 'D': 355, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 391, 'D': 391, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 379, 'D': 379, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 381, 'D': 381, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 11, 'DIST': 16, 'D': 4, 'F': 1}, 'samples_num500000': {'I': 9, 'DIST': 19, 'D': 6, 'F': 4}, 'samples_num100000': {'I': 2, 'DIST': 10, 'D': 3, 'F': 5}, 'samples_num3000000': {'I': 11, 'DIST': 16, 'D': 4, 'F': 1}, 'samples_num2000000': {'I': 12, 'DIST': 19, 'D': 5, 'F': 2}, 'samples_num1000000': {'I': 5, 'DIST': 13, 'D': 6, 'F': 2}}, 'error5': {'samples_num4000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 22, 'DIST': 22, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 21, 'DIST': 23, 'D': 0, 'F': 2}, 'samples_num3000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}, 'samples_num1000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}}, 'error7': {'samples_num4000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 17, 'DIST': 19, 'D': 0, 'F': 2}, 'samples_num100000': {'I': 21, 'DIST': 22, 'D': 0, 'F': 1}, 'samples_num3000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}, 'samples_num1000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}}}, 'window_size30': {'error5': {'samples_num4000000': {'I': 17, 'DIST': 18, 'D': 1, 'F': 0}, 'samples_num500000': {'I': 4, 'DIST': 4, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 1, 'DIST': 1, 'D': 0, 'F': 0}, 'samples_num3000000': {'I': 25, 'DIST': 25, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 21, 'DIST': 24, 'D': 2, 'F': 1}, 'samples_num1000000': {'I': 4, 'DIST': 4, 'D': 0, 'F': 0}}, 'error7': {'samples_num500000': {'I': 2, 'DIST': 3, 'D': 1, 'F': 0}, 'samples_num2000000': {'I': 17, 'DIST': 22, 'D': 0, 'F': 5}, 'samples_num3000000': {'I': 19, 'DIST': 19, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 9, 'D': 9, 'F': 0}, 'samples_num1000000': {'I': 2, 'DIST': 10, 'D': 0, 'F': 8}}}}, 'sample_len40': {'window_size20': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 466, 'D': 466, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 453, 'D': 453, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 439, 'D': 439, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 462, 'D': 462, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 459, 'D': 459, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 453, 'D': 453, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 37, 'DIST': 38, 'D': 0, 'F': 1}, 'samples_num500000': {'I': 25, 'DIST': 26, 'D': 0, 'F': 1}, 'samples_num100000': {'I': 1, 'DIST': 156, 'D': 117, 'F': 38}, 'samples_num3000000': {'I': 22, 'DIST': 23, 'D': 0, 'F': 1}, 'samples_num2000000': {'I': 34, 'DIST': 35, 'D': 0, 'F': 1}, 'samples_num1000000': {'I': 28, 'DIST': 30, 'D': 1, 'F': 1}}, 'error5': {'samples_num4000000': {'I': 18, 'DIST': 20, 'D': 0, 'F': 2}, 'samples_num500000': {'I': 14, 'DIST': 15, 'D': 1, 'F': 0}, 'samples_num100000': {'I': 5, 'DIST': 7, 'D': 0, 'F': 2}, 'samples_num3000000': {'I': 20, 'DIST': 22, 'D': 1, 'F': 1}, 'samples_num2000000': {'I': 24, 'DIST': 25, 'D': 1, 'F': 0}, 'samples_num1000000': {'I': 20, 'DIST': 22, 'D': 0, 'F': 2}}, 'error7': {'samples_num4000000': {'I': 9, 'DIST': 10, 'D': 0, 'F': 1}, 'samples_num500000': {'I': 17, 'DIST': 18, 'D': 1, 'F': 0}, 'samples_num100000': {'I': 40, 'DIST': 40, 'D': 0, 'F': 0}, 'samples_num3000000': {'I': 9, 'DIST': 9, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 12, 'DIST': 13, 'D': 0, 'F': 1}, 'samples_num1000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}}}, 'window_size30': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 454, 'D': 454, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 455, 'D': 455, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 460, 'D': 460, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 464, 'D': 464, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 446, 'D': 446, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 461, 'D': 461, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 3, 'DIST': 6, 'D': 2, 'F': 1}, 'samples_num500000': {'I': 0, 'DIST': 446, 'D': 446, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 471, 'D': 471, 'F': 0}, 'samples_num3000000': {'I': 1, 'DIST': 126, 'D': 124, 'F': 1}, 'samples_num2000000': {'I': 0, 'DIST': 338, 'D': 338, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 402, 'D': 402, 'F': 0}}, 'error5': {'samples_num4000000': {'I': 5, 'DIST': 13, 'D': 0, 'F': 8}, 'samples_num500000': {'I': 2, 'DIST': 2, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1, 'D': 0, 'F': 1}, 'samples_num3000000': {'I': 5, 'DIST': 12, 'D': 0, 'F': 7}, 'samples_num2000000': {'I': 4, 'DIST': 5, 'D': 0, 'F': 1}, 'samples_num1000000': {'I': 2, 'DIST': 2, 'D': 0, 'F': 0}}, 'error7': {'samples_num4000000': {'I': 7, 'DIST': 10, 'D': 1, 'F': 2}, 'samples_num500000': {'I': 2, 'DIST': 4, 'D': 2, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 374, 'D': 374, 'F': 0}, 'samples_num3000000': {'I': 4, 'DIST': 4, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 5, 'DIST': 12, 'D': 0, 'F': 7}, 'samples_num1000000': {'I': 3, 'DIST': 5, 'D': 2, 'F': 0}}}}, 'sample_len50': {'window_size20': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 419, 'D': 419, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 410, 'D': 410, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 439, 'D': 439, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 417, 'D': 417, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 436, 'D': 436, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 431, 'D': 431, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 54, 'DIST': 61, 'D': 0, 'F': 7}, 'samples_num100000': {'I': 94, 'DIST': 96, 'D': 0, 'F': 2}, 'samples_num3000000': {'I': 7, 'DIST': 7, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 32, 'DIST': 33, 'D': 1, 'F': 0}, 'samples_num1000000': {'I': 21, 'DIST': 22, 'D': 0, 'F': 1}}, 'error5': {'samples_num4000000': {'I': 21, 'DIST': 21, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 24, 'DIST': 26, 'D': 0, 'F': 2}, 'samples_num100000': {'I': 11, 'DIST': 13, 'D': 1, 'F': 1}, 'samples_num3000000': {'I': 21, 'DIST': 21, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 18, 'DIST': 19, 'D': 0, 'F': 1}, 'samples_num1000000': {'I': 8, 'DIST': 9, 'D': 0, 'F': 1}}, 'error7': {'samples_num4000000': {'I': 9, 'DIST': 9, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 19, 'DIST': 20, 'D': 0, 'F': 1}, 'samples_num100000': {'I': 20, 'DIST': 23, 'D': 1, 'F': 2}, 'samples_num3000000': {'I': 20, 'DIST': 23, 'D': 0, 'F': 3}, 'samples_num2000000': {'I': 20, 'DIST': 23, 'D': 0, 'F': 3}, 'samples_num1000000': {'I': 18, 'DIST': 20, 'D': 0, 'F': 2}}}, 'window_size30': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 456, 'D': 456, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 422, 'D': 422, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 438, 'D': 438, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 455, 'D': 455, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 441, 'D': 441, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 434, 'D': 434, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 4, 'DIST': 9, 'D': 3, 'F': 2}, 'samples_num500000': {'I': 0, 'DIST': 391, 'D': 391, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 459, 'D': 459, 'F': 0}, 'samples_num3000000': {'I': 1, 'DIST': 101, 'D': 100, 'F': 0}, 'samples_num2000000': {'I': 4, 'DIST': 10, 'D': 4, 'F': 2}, 'samples_num1000000': {'I': 0, 'DIST': 366, 'D': 366, 'F': 0}}, 'error5': {'samples_num4000000': {'I': 6, 'DIST': 10, 'D': 0, 'F': 4}, 'samples_num500000': {'I': 2, 'DIST': 2, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 1, 'DIST': 1, 'D': 0, 'F': 0}, 'samples_num3000000': {'I': 7, 'DIST': 11, 'D': 2, 'F': 2}, 'samples_num2000000': {'I': 4, 'DIST': 12, 'D': 0, 'F': 8}, 'samples_num1000000': {'I': 3, 'DIST': 4, 'D': 0, 'F': 1}}, 'error7': {'samples_num4000000': {'I': 18, 'DIST': 22, 'D': 1, 'F': 3}, 'samples_num500000': {'I': 1, 'DIST': 1, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 357, 'D': 357, 'F': 0}, 'samples_num3000000': {'I': 11, 'DIST': 12, 'D': 0, 'F': 1}, 'samples_num2000000': {'I': 11, 'DIST': 12, 'D': 0, 'F': 1}, 'samples_num1000000': {'I': 2, 'DIST': 2, 'D': 0, 'F': 0}}}}}}
        key_length_vec = [512]
        sample_len_vec = [31,40,50,100]
        # megic_num_vec = [10, 30, 50]
        samples_num_vec = [100000, 500000, 1000000, 2000000, 3000000, 4000000]
        stitch_vec = [1]
        window_size_vec=[20,30] #each has its own graph
        quantile_vec=[0.5] #each has its own graph

        stitch_shift_size = 1
        # window_size = 30
        quantile = 0.6
        # sample_len = 50
        # key_length = 512
        # GRAPHS = "KEYLENGTH" #"WINDOES" # QUANTILE
        # X = "megicNumVec"

        error_vec = [5 , 7 , 9, 10 ]


        workbook = xlsxwriter.Workbook('./simulation_table512.xlsx')
        worksheet = workbook.add_worksheet()


        for key_length in key_length_vec:
            for sample_len in sample_len_vec:
                if sample_len == 31:
                    row = 0
                for window_size in window_size_vec:
                    if window_size == 20:
                        col = 0
                    # if window_size ==30:
                    #     col = 24
                    for error in error_vec:
                        # if error == 5:
                        #     col +=0

                        for samples_num in samples_num_vec:
                            try:
                                item = tableResult["key_length{0}".format(key_length)]["sample_len{0}".format(sample_len)][
                                "window_size{0}".format(window_size)]["error{0}".format(error)][
                                "samples_num{0}".format(samples_num)]

                                worksheet.write(row, col, int(item['DIST']))
                                worksheet.write(row+1, col, str(item))


                                debug = "key_length{0}_sample_len{1}_window_size{2}_error{3}_samples_num{4}".format(key_length,sample_len,window_size,error,samples_num)
                                worksheet.write(row+2, col, str(debug))


                            except:
                                pass
                            col +=1
                        # col +=5

                row +=3

        workbook.close()


    if REAL:
        hex_key_512 = "023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd"
        key = ''.join(func.hex2bin_map[i] for i in hex_key_512)

        key_length_vec = [len(key)]
        probe_len_vec = [170, 230, 300, 500]


        tableResult = {'key_length512': {'probe_len230': {'window_size20': {'errorREAL': {'samples_num4000000': {'I': 1, 'DIST': 183, 'D': 164, 'F': 18}, 'samples_num500000': {'I': 1, 'DIST': 184, 'D': 162, 'F': 21}, 'samples_num100000': {'I': 1, 'DIST': 184, 'D': 161, 'F': 22}, 'samples_num3000000': {'I': 1, 'DIST': 183, 'D': 164, 'F': 18}, 'samples_num2000000': {'I': 1, 'DIST': 184, 'D': 161, 'F': 22}, 'samples_num5000000': {'I': 1, 'DIST': 183, 'D': 164, 'F': 18}, 'samples_num1000000': {'I': 1, 'DIST': 187, 'D': 165, 'F': 21}}}, 'window_size30': {'errorREAL': {'samples_num4000000': {'I': 13, 'DIST': 45, 'D': 31, 'F': 1}, 'samples_num500000': {'I': 8, 'DIST': 42, 'D': 33, 'F': 1}, 'samples_num100000': {'I': 7, 'DIST': 45, 'D': 37, 'F': 1}, 'samples_num3000000': {'I': 13, 'DIST': 45, 'D': 31, 'F': 1}, 'samples_num2000000': {'I': 12, 'DIST': 44, 'D': 31, 'F': 1}, 'samples_num5000000': {'I': 13, 'DIST': 45, 'D': 31, 'F': 1}, 'samples_num1000000': {'I': 13, 'DIST': 48, 'D': 28, 'F': 7}}}}, 'probe_len170': {'window_size20': {'errorREAL': {'samples_num1000': {'I': 0, 'DIST': 410, 'D': 410, 'F': 0}, 'samples_num5000': {'I': 0, 'DIST': 290, 'D': 290, 'F': 0}, 'samples_num10000': {'I': 0, 'DIST': 290, 'D': 290, 'F': 0}, 'samples_num20000': {'I': 0, 'DIST': 250, 'D': 250, 'F': 0}, 'samples_num30000': {'I': 0, 'DIST': 283, 'D': 283, 'F': 0}}}, 'window_size30': {'errorREAL': {'samples_num1000': {'I': 0, 'DIST': 476, 'D': 476, 'F': 0}, 'samples_num5000': {'I': 0, 'DIST': 471, 'D': 471, 'F': 0}, 'samples_num10000': {'I': 0, 'DIST': 465, 'D': 465, 'F': 0}, 'samples_num20000': {'I': 0, 'DIST': 459, 'D': 459, 'F': 0}, 'samples_num30000': {'I': 0, 'DIST': 459, 'D': 459, 'F': 0}}}}, 'probe_len500': {'window_size20': {'errorREAL': {'samples_num40000': {'I': 0, 'DIST': 219, 'D': 219, 'F': 0}, 'samples_num20000': {'I': 0, 'DIST': 233, 'D': 233, 'F': 0}, 'samples_num10000': {'I': 0, 'DIST': 301, 'D': 301, 'F': 0}, 'samples_num50000': {'I': 0, 'DIST': 220, 'D': 220, 'F': 0}, 'samples_num30000': {'I': 0, 'DIST': 218, 'D': 218, 'F': 0}}}, 'window_size30': {'errorREAL': {'samples_num40000': {'I': 0, 'DIST': 452, 'D': 452, 'F': 0}, 'samples_num20000': {'I': 0, 'DIST': 460, 'D': 460, 'F': 0}, 'samples_num10000': {'I': 0, 'DIST': 460, 'D': 460, 'F': 0}, 'samples_num50000': {'I': 0, 'DIST': 454, 'D': 454, 'F': 0}, 'samples_num30000': {'I': 0, 'DIST': 455, 'D': 455, 'F': 0}}}}, 'probe_len300': {'window_size20': {'errorREAL': {'samples_num4000000': {'I': 0, 'DIST': 252, 'D': 252, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 305, 'D': 305, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 275, 'D': 275, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 231, 'D': 228, 'F': 3}, 'samples_num2000000': {'I': 0, 'DIST': 231, 'D': 228, 'F': 3}, 'samples_num5000000': {'I': 0, 'DIST': 252, 'D': 252, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 235, 'D': 235, 'F': 0}}}, 'window_size30': {'errorREAL': {'samples_num4000000': {'I': 73, 'DIST': 97, 'D': 17, 'F': 7}, 'samples_num500000': {'I': 1, 'DIST': 179, 'D': 143, 'F': 35}, 'samples_num100000': {'I': 0, 'DIST': 315, 'D': 315, 'F': 0}, 'samples_num3000000': {'I': 41, 'DIST': 67, 'D': 24, 'F': 2}, 'samples_num2000000': {'I': 32, 'DIST': 62, 'D': 24, 'F': 6}, 'samples_num5000000': {'I': 73, 'DIST': 97, 'D': 17, 'F': 7}, 'samples_num1000000': {'I': 23, 'DIST': 58, 'D': 24, 'F': 11}}}}}}

        samples_num_vec = [100000, 500000, 1000000, 2000000, 3000000, 4000000, 5000000]
        stitch_vec = [1]
        window_size_vec=[20,30] #each has its own graph
        quantile_vec=[0.5] #each has its own graph

        stitch_shift_size = 1
        quantile = 0.6

        error_vec = ["REAL"]


        workbook = xlsxwriter.Workbook('./real_table512.xlsx')
        worksheet = workbook.add_worksheet()

        for key_length in key_length_vec:
            for probe_len in probe_len_vec:
                if probe_len == 170:
                    row = 0
                for window_size in window_size_vec:
                    if window_size == 20:
                        col = 0
                    # if window_size ==30:
                    #     col = 24
                    for error in error_vec:
                        # if error == 5:
                        #     col +=0

                        for samples_num in samples_num_vec:
                            try:
                                item = tableResult["key_length{0}".format(key_length)]["probe_len{0}".format(probe_len)][
                                "window_size{0}".format(window_size)]["error{0}".format(error)][
                                "samples_num{0}".format(samples_num)]

                                worksheet.write(row, col, int(item['DIST']))
                                worksheet.write(row+1, col, str(item))


                                debug = "key_length{0}_probe_len{1}_window_size{2}_error{3}_samples_num{4}".format(key_length,probe_len,window_size,error,samples_num)
                                worksheet.write(row+2, col, str(debug))


                            except:
                                pass
                            col +=1
                        # col +=5

                row +=3

        workbook.close()




    x=1




