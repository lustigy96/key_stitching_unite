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
import key_stitching_unite.key_stitching_functinos as func



if __name__ == "__main__":
    SIMULATION = True

    REAL = False
    # DATA_FILE_PATH = "./results/simulation/table.txt"
    # with open(DATA_FILE_PATH, "r") as dataFile:
    #     str = dataFile.read()
    #
    # tableDictResult = yaml.load(str)
    # print tableDictResult


    if SIMULATION:

        # tableResult = {'key_length2048': {'sample_len31': {'window_size20': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 1979, 'D': 1979, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 1976, 'D': 1976, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1997, 'D': 1997, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 1965, 'D': 1965, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 1995, 'D': 1995, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 2001, 'D': 2001, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 39, 'DIST': 550, 'D': 467, 'F': 44}, 'samples_num500000': {'I': 0, 'DIST': 1830, 'D': 1830, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1982, 'D': 1982, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 670, 'D': 667, 'F': 3}, 'samples_num2000000': {'I': 0, 'DIST': 1009, 'D': 1007, 'F': 2}, 'samples_num1000000': {'I': 0, 'DIST': 1684, 'D': 1684, 'F': 0}}, 'error5': {'samples_num4000000': {'I': 13, 'DIST': 13, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 9, 'DIST': 9, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 10, 'DIST': 10, 'D': 0, 'F': 0}, 'samples_num3000000': {'I': 6, 'DIST': 6, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 6, 'DIST': 9, 'D': 0, 'F': 3}, 'samples_num1000000': {'I': 5, 'DIST': 6, 'D': 1, 'F': 0}}, 'error7': {'samples_num4000000': {'I': 8, 'DIST': 8, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 28, 'DIST': 30, 'D': 0, 'F': 2}, 'samples_num100000': {'I': 0, 'DIST': 1702, 'D': 1702, 'F': 0}, 'samples_num3000000': {'I': 28, 'DIST': 28, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 13, 'DIST': 13, 'D': 0, 'F': 0}, 'samples_num1000000': {'I': 15, 'DIST': 15, 'D': 0, 'F': 0}}}, 'window_size30': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 2007, 'D': 2007, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 2007, 'D': 2007, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 2004, 'D': 2004, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 2003, 'D': 2003, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 2008, 'D': 2008, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 2004, 'D': 2004, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 0, 'DIST': 2003, 'D': 2003, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 2015, 'D': 2015, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 2017, 'D': 2017, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 2009, 'D': 2009, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 2012, 'D': 2012, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 2012, 'D': 2012, 'F': 0}}, 'error5': {'samples_num4000000': {'I': 2, 'DIST': 3, 'D': 0, 'F': 1}, 'samples_num500000': {'I': 0, 'DIST': 1728, 'D': 1728, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 2005, 'D': 2005, 'F': 0}, 'samples_num3000000': {'I': 2, 'DIST': 3, 'D': 0, 'F': 1}, 'samples_num2000000': {'I': 2, 'DIST': 2, 'D': 0, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 1197, 'D': 1197, 'F': 0}}, 'error7': {'samples_num4000000': {'I': 0, 'DIST': 1808, 'D': 1808, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 2008, 'D': 2008, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 2015, 'D': 2015, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 1828, 'D': 1828, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 1930, 'D': 1930, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 1985, 'D': 1985, 'F': 0}}}}, 'sample_len100': {'window_size20': {'error9': {'samples_num500000': {'I': 0, 'DIST': 1928, 'D': 1928, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1936, 'D': 1936, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 1890, 'D': 1890, 'F': 0}}, 'error10': {'samples_num500000': {'I': 8, 'DIST': 668, 'D': 505, 'F': 155}, 'samples_num100000': {'I': 0, 'DIST': 1595, 'D': 1595, 'F': 0}, 'samples_num1000000': {'I': 1, 'DIST': 372, 'D': 367, 'F': 4}}, 'error5': {'samples_num500000': {'I': 6, 'DIST': 677, 'D': 524, 'F': 147}, 'samples_num100000': {'I': 6, 'DIST': 678, 'D': 525, 'F': 147}, 'samples_num1000000': {'I': 6, 'DIST': 677, 'D': 527, 'F': 144}}, 'error7': {'samples_num500000': {'I': 6, 'DIST': 674, 'D': 523, 'F': 145}, 'samples_num100000': {'I': 6, 'DIST': 671, 'D': 514, 'F': 151}, 'samples_num1000000': {'I': 6, 'DIST': 674, 'D': 519, 'F': 149}}}, 'window_size30': {'error9': {'samples_num500000': {'I': 0, 'DIST': 1856, 'D': 1856, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1871, 'D': 1871, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 1938, 'D': 1938, 'F': 0}}, 'error10': {'samples_num500000': {'I': 0, 'DIST': 1931, 'D': 1931, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1992, 'D': 1992, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 1826, 'D': 1826, 'F': 0}}, 'error5': {'samples_num500000': {'I': 0, 'DIST': 0, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 8, 'D': 5, 'F': 3}, 'samples_num1000000': {'I': 4, 'DIST': 5, 'D': 0, 'F': 1}}, 'error7': {'samples_num500000': {'I': 0, 'DIST': 0, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1827, 'D': 1827, 'F': 0}, 'samples_num1000000': {'I': 1, 'DIST': 1, 'D': 0, 'F': 0}}}}, 'sample_len40': {'window_size20': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 1975, 'D': 1975, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 1987, 'D': 1987, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1977, 'D': 1977, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 1950, 'D': 1950, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 1951, 'D': 1951, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 1959, 'D': 1959, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 0, 'DIST': 549, 'D': 549, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 1659, 'D': 1659, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1892, 'D': 1892, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 552, 'D': 552, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 599, 'D': 599, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 1267, 'D': 1267, 'F': 0}}, 'error5': {'samples_num4000000': {'I': 7, 'DIST': 7, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 5, 'DIST': 8, 'D': 0, 'F': 3}, 'samples_num100000': {'I': 11, 'DIST': 12, 'D': 0, 'F': 1}, 'samples_num3000000': {'I': 8, 'DIST': 9, 'D': 0, 'F': 1}, 'samples_num2000000': {'I': 8, 'DIST': 9, 'D': 0, 'F': 1}, 'samples_num1000000': {'I': 7, 'DIST': 8, 'D': 1, 'F': 0}}, 'error7': {'samples_num4000000': {'I': 2, 'DIST': 3, 'D': 1, 'F': 0}, 'samples_num500000': {'I': 28, 'DIST': 28, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 5, 'DIST': 414, 'D': 409, 'F': 0}, 'samples_num3000000': {'I': 5, 'DIST': 6, 'D': 0, 'F': 1}, 'samples_num2000000': {'I': 10, 'DIST': 11, 'D': 0, 'F': 1}, 'samples_num1000000': {'I': 5, 'DIST': 7, 'D': 0, 'F': 2}}}, 'window_size30': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 1990, 'D': 1990, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 1976, 'D': 1976, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1972, 'D': 1972, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 1985, 'D': 1985, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 1985, 'D': 1985, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 1984, 'D': 1984, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 0, 'DIST': 1935, 'D': 1935, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 2003, 'D': 2003, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 2009, 'D': 2009, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 1956, 'D': 1956, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 1975, 'D': 1975, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 1991, 'D': 1991, 'F': 0}}, 'error5': {'samples_num4000000': {'I': 3, 'DIST': 4, 'D': 0, 'F': 1}, 'samples_num500000': {'I': 1, 'DIST': 1, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1682, 'D': 1682, 'F': 0}, 'samples_num3000000': {'I': 5, 'DIST': 9, 'D': 0, 'F': 4}, 'samples_num2000000': {'I': 3, 'DIST': 5, 'D': 1, 'F': 1}, 'samples_num1000000': {'I': 1, 'DIST': 1, 'D': 0, 'F': 0}}, 'error7': {'samples_num4000000': {'I': 5, 'DIST': 8, 'D': 3, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 1839, 'D': 1839, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1996, 'D': 1996, 'F': 0}, 'samples_num3000000': {'I': 2, 'DIST': 3, 'D': 0, 'F': 1}, 'samples_num2000000': {'I': 2, 'DIST': 3, 'D': 0, 'F': 1}, 'samples_num1000000': {'I': 0, 'DIST': 1588, 'D': 1588, 'F': 0}}}}, 'sample_len50': {'window_size20': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 1954, 'D': 1954, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 1962, 'D': 1962, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1936, 'D': 1936, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 1958, 'D': 1958, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 1960, 'D': 1960, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 1942, 'D': 1942, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 0, 'DIST': 546, 'D': 546, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 898, 'D': 878, 'F': 20}, 'samples_num100000': {'I': 0, 'DIST': 1853, 'D': 1853, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 558, 'D': 558, 'F': 0}, 'samples_num2000000': {'I': 6, 'DIST': 589, 'D': 583, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 867, 'D': 866, 'F': 1}}, 'error5': {'samples_num4000000': {'I': 5, 'DIST': 8, 'D': 0, 'F': 3}, 'samples_num500000': {'I': 4, 'DIST': 4, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1, 'D': 1, 'F': 0}, 'samples_num3000000': {'I': 7, 'DIST': 9, 'D': 0, 'F': 2}, 'samples_num2000000': {'I': 7, 'DIST': 8, 'D': 1, 'F': 0}, 'samples_num1000000': {'I': 7, 'DIST': 9, 'D': 0, 'F': 2}}, 'error7': {'samples_num4000000': {'I': 15, 'DIST': 15, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 0, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 24, 'DIST': 741, 'D': 716, 'F': 1}, 'samples_num3000000': {'I': 15, 'DIST': 15, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 10, 'DIST': 11, 'D': 0, 'F': 1}, 'samples_num1000000': {'I': 14, 'DIST': 14, 'D': 0, 'F': 0}}}, 'window_size30': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 1971, 'D': 1971, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 1972, 'D': 1972, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1965, 'D': 1965, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 1925, 'D': 1925, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 1975, 'D': 1975, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 1970, 'D': 1970, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 0, 'DIST': 1859, 'D': 1859, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 1988, 'D': 1988, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 2007, 'D': 2007, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 1897, 'D': 1897, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 1925, 'D': 1925, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 1962, 'D': 1962, 'F': 0}}, 'error5': {'samples_num4000000': {'I': 13, 'DIST': 13, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 1, 'DIST': 1, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 235, 'D': 235, 'F': 0}, 'samples_num3000000': {'I': 14, 'DIST': 14, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 3, 'DIST': 4, 'D': 0, 'F': 1}, 'samples_num1000000': {'I': 1, 'DIST': 1, 'D': 0, 'F': 0}}, 'error7': {'samples_num4000000': {'I': 3, 'DIST': 3, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 1334, 'D': 1334, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1961, 'D': 1961, 'F': 0}, 'samples_num3000000': {'I': 4, 'DIST': 6, 'D': 1, 'F': 1}, 'samples_num2000000': {'I': 2, 'DIST': 5, 'D': 1, 'F': 2}, 'samples_num1000000': {'I': 1, 'DIST': 2, 'D': 1, 'F': 0}}}}}}
        # key_length_vec = [2048]
        tableResult = {'key_length512': {'sample_len31': {'window_size20': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 471, 'D': 471, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 469, 'D': 469, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 464, 'D': 464, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 461, 'D': 461, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 465, 'D': 465, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 453, 'D': 453, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 43, 'DIST': 43, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 66, 'DIST': 66, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 364, 'D': 364, 'F': 0}, 'samples_num3000000': {'I': 47, 'DIST': 47, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 35, 'DIST': 35, 'D': 0, 'F': 0}, 'samples_num1000000': {'I': 48, 'DIST': 48, 'D': 0, 'F': 0}}, 'error5': {'samples_num4000000': {'I': 29, 'DIST': 29, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 24, 'DIST': 24, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 12, 'DIST': 12, 'D': 0, 'F': 0}, 'samples_num3000000': {'I': 29, 'DIST': 29, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 28, 'DIST': 28, 'D': 0, 'F': 0}, 'samples_num1000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}}, 'error7': {'samples_num4000000': {'I': 38, 'DIST': 38, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 18, 'DIST': 18, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 15, 'DIST': 15, 'D': 0, 'F': 0}, 'samples_num3000000': {'I': 31, 'DIST': 31, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 28, 'DIST': 28, 'D': 0, 'F': 0}, 'samples_num1000000': {'I': 13, 'DIST': 14, 'D': 0, 'F': 1}}}, 'window_size30': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 477, 'D': 477, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 474, 'D': 474, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 475, 'D': 475, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 476, 'D': 476, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 476, 'D': 476, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 477, 'D': 477, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 0, 'DIST': 442, 'D': 442, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 478, 'D': 478, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 480, 'D': 480, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 448, 'D': 448, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 461, 'D': 461, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 474, 'D': 474, 'F': 0}}, 'error5': {'samples_num4000000': {'I': 4, 'DIST': 4, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 1, 'DIST': 1, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 387, 'D': 387, 'F': 0}, 'samples_num3000000': {'I': 3, 'DIST': 4, 'D': 0, 'F': 1}, 'samples_num2000000': {'I': 3, 'DIST': 3, 'D': 0, 'F': 0}, 'samples_num1000000': {'I': 2, 'DIST': 2, 'D': 0, 'F': 0}}, 'error7': {'samples_num4000000': {'I': 3, 'DIST': 3, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 410, 'D': 410, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 474, 'D': 474, 'F': 0}, 'samples_num3000000': {'I': 3, 'DIST': 4, 'D': 0, 'F': 1}, 'samples_num2000000': {'I': 2, 'DIST': 3, 'D': 1, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 258, 'D': 258, 'F': 0}}}}, 'sample_len40': {'window_size20': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 466, 'D': 466, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 453, 'D': 453, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 439, 'D': 439, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 462, 'D': 462, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 459, 'D': 459, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 453, 'D': 453, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 37, 'DIST': 38, 'D': 0, 'F': 1}, 'samples_num500000': {'I': 25, 'DIST': 26, 'D': 0, 'F': 1}, 'samples_num100000': {'I': 1, 'DIST': 156, 'D': 117, 'F': 38}, 'samples_num3000000': {'I': 22, 'DIST': 23, 'D': 0, 'F': 1}, 'samples_num2000000': {'I': 34, 'DIST': 35, 'D': 0, 'F': 1}, 'samples_num1000000': {'I': 28, 'DIST': 30, 'D': 1, 'F': 1}}, 'error5': {'samples_num4000000': {'I': 18, 'DIST': 20, 'D': 0, 'F': 2}, 'samples_num500000': {'I': 14, 'DIST': 15, 'D': 1, 'F': 0}, 'samples_num100000': {'I': 5, 'DIST': 7, 'D': 0, 'F': 2}, 'samples_num3000000': {'I': 20, 'DIST': 22, 'D': 1, 'F': 1}, 'samples_num2000000': {'I': 24, 'DIST': 25, 'D': 1, 'F': 0}, 'samples_num1000000': {'I': 20, 'DIST': 22, 'D': 0, 'F': 2}}, 'error7': {'samples_num4000000': {'I': 9, 'DIST': 10, 'D': 0, 'F': 1}, 'samples_num500000': {'I': 17, 'DIST': 18, 'D': 1, 'F': 0}, 'samples_num100000': {'I': 40, 'DIST': 40, 'D': 0, 'F': 0}, 'samples_num3000000': {'I': 9, 'DIST': 9, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 12, 'DIST': 13, 'D': 0, 'F': 1}, 'samples_num1000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}}}, 'window_size30': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 454, 'D': 454, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 455, 'D': 455, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 460, 'D': 460, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 464, 'D': 464, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 446, 'D': 446, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 461, 'D': 461, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 3, 'DIST': 6, 'D': 2, 'F': 1}, 'samples_num500000': {'I': 0, 'DIST': 446, 'D': 446, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 471, 'D': 471, 'F': 0}, 'samples_num3000000': {'I': 1, 'DIST': 126, 'D': 124, 'F': 1}, 'samples_num2000000': {'I': 0, 'DIST': 338, 'D': 338, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 402, 'D': 402, 'F': 0}}, 'error5': {'samples_num4000000': {'I': 5, 'DIST': 13, 'D': 0, 'F': 8}, 'samples_num500000': {'I': 2, 'DIST': 2, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 1, 'D': 0, 'F': 1}, 'samples_num3000000': {'I': 5, 'DIST': 12, 'D': 0, 'F': 7}, 'samples_num2000000': {'I': 4, 'DIST': 5, 'D': 0, 'F': 1}, 'samples_num1000000': {'I': 2, 'DIST': 2, 'D': 0, 'F': 0}}, 'error7': {'samples_num4000000': {'I': 7, 'DIST': 10, 'D': 1, 'F': 2}, 'samples_num500000': {'I': 2, 'DIST': 4, 'D': 2, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 374, 'D': 374, 'F': 0}, 'samples_num3000000': {'I': 4, 'DIST': 4, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 5, 'DIST': 12, 'D': 0, 'F': 7}, 'samples_num1000000': {'I': 3, 'DIST': 5, 'D': 2, 'F': 0}}}}, 'sample_len100': {'window_size20': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 362, 'D': 362, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 386, 'D': 386, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 355, 'D': 355, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 391, 'D': 391, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 379, 'D': 379, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 381, 'D': 381, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 11, 'DIST': 16, 'D': 4, 'F': 1}, 'samples_num500000': {'I': 9, 'DIST': 19, 'D': 6, 'F': 4}, 'samples_num100000': {'I': 2, 'DIST': 10, 'D': 3, 'F': 5}, 'samples_num3000000': {'I': 11, 'DIST': 16, 'D': 4, 'F': 1}, 'samples_num2000000': {'I': 12, 'DIST': 19, 'D': 5, 'F': 2}, 'samples_num1000000': {'I': 5, 'DIST': 13, 'D': 6, 'F': 2}}, 'error5': {'samples_num4000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 22, 'DIST': 22, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 21, 'DIST': 23, 'D': 0, 'F': 2}, 'samples_num3000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}, 'samples_num1000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}}, 'error7': {'samples_num4000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 17, 'DIST': 19, 'D': 0, 'F': 2}, 'samples_num100000': {'I': 21, 'DIST': 22, 'D': 0, 'F': 1}, 'samples_num3000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}, 'samples_num1000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}}}, 'window_size30': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 405, 'D': 405, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 387, 'D': 387, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 384, 'D': 384, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 397, 'D': 397, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 357, 'D': 357, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 367, 'D': 367, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 31, 'DIST': 32, 'D': 0, 'F': 1}, 'samples_num500000': {'I': 0, 'DIST': 103, 'D': 100, 'F': 3}, 'samples_num100000': {'I': 0, 'DIST': 420, 'D': 420, 'F': 0}, 'samples_num3000000': {'I': 42, 'DIST': 43, 'D': 0, 'F': 1}, 'samples_num2000000': {'I': 2, 'DIST': 13, 'D': 4, 'F': 7}, 'samples_num1000000': {'I': 0, 'DIST': 16, 'D': 14, 'F': 2}}, 'error5': {'samples_num4000000': {'I': 17, 'DIST': 18, 'D': 1, 'F': 0}, 'samples_num500000': {'I': 4, 'DIST': 4, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 1, 'DIST': 1, 'D': 0, 'F': 0}, 'samples_num3000000': {'I': 25, 'DIST': 25, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 21, 'DIST': 24, 'D': 2, 'F': 1}, 'samples_num1000000': {'I': 4, 'DIST': 4, 'D': 0, 'F': 0}}, 'error7': {'samples_num4000000': {'I': 22, 'DIST': 22, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 2, 'DIST': 3, 'D': 1, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 9, 'D': 9, 'F': 0}, 'samples_num3000000': {'I': 19, 'DIST': 19, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 17, 'DIST': 22, 'D': 0, 'F': 5}, 'samples_num1000000': {'I': 2, 'DIST': 10, 'D': 0, 'F': 8}}}}, 'sample_len50': {'window_size20': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 419, 'D': 419, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 410, 'D': 410, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 439, 'D': 439, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 417, 'D': 417, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 436, 'D': 436, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 431, 'D': 431, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 17, 'DIST': 17, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 54, 'DIST': 61, 'D': 0, 'F': 7}, 'samples_num100000': {'I': 94, 'DIST': 96, 'D': 0, 'F': 2}, 'samples_num3000000': {'I': 7, 'DIST': 7, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 32, 'DIST': 33, 'D': 1, 'F': 0}, 'samples_num1000000': {'I': 21, 'DIST': 22, 'D': 0, 'F': 1}}, 'error5': {'samples_num4000000': {'I': 21, 'DIST': 21, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 24, 'DIST': 26, 'D': 0, 'F': 2}, 'samples_num100000': {'I': 11, 'DIST': 13, 'D': 1, 'F': 1}, 'samples_num3000000': {'I': 21, 'DIST': 21, 'D': 0, 'F': 0}, 'samples_num2000000': {'I': 18, 'DIST': 19, 'D': 0, 'F': 1}, 'samples_num1000000': {'I': 8, 'DIST': 9, 'D': 0, 'F': 1}}, 'error7': {'samples_num4000000': {'I': 9, 'DIST': 9, 'D': 0, 'F': 0}, 'samples_num500000': {'I': 19, 'DIST': 20, 'D': 0, 'F': 1}, 'samples_num100000': {'I': 20, 'DIST': 23, 'D': 1, 'F': 2}, 'samples_num3000000': {'I': 20, 'DIST': 23, 'D': 0, 'F': 3}, 'samples_num2000000': {'I': 20, 'DIST': 23, 'D': 0, 'F': 3}, 'samples_num1000000': {'I': 18, 'DIST': 20, 'D': 0, 'F': 2}}}, 'window_size30': {'error9': {'samples_num4000000': {'I': 0, 'DIST': 456, 'D': 456, 'F': 0}, 'samples_num500000': {'I': 0, 'DIST': 422, 'D': 422, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 438, 'D': 438, 'F': 0}, 'samples_num3000000': {'I': 0, 'DIST': 455, 'D': 455, 'F': 0}, 'samples_num2000000': {'I': 0, 'DIST': 441, 'D': 441, 'F': 0}, 'samples_num1000000': {'I': 0, 'DIST': 434, 'D': 434, 'F': 0}}, 'error10': {'samples_num4000000': {'I': 4, 'DIST': 9, 'D': 3, 'F': 2}, 'samples_num500000': {'I': 0, 'DIST': 391, 'D': 391, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 459, 'D': 459, 'F': 0}, 'samples_num3000000': {'I': 1, 'DIST': 101, 'D': 100, 'F': 0}, 'samples_num2000000': {'I': 4, 'DIST': 10, 'D': 4, 'F': 2}, 'samples_num1000000': {'I': 0, 'DIST': 366, 'D': 366, 'F': 0}}, 'error5': {'samples_num4000000': {'I': 6, 'DIST': 10, 'D': 0, 'F': 4}, 'samples_num500000': {'I': 2, 'DIST': 2, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 1, 'DIST': 1, 'D': 0, 'F': 0}, 'samples_num3000000': {'I': 7, 'DIST': 11, 'D': 2, 'F': 2}, 'samples_num2000000': {'I': 4, 'DIST': 12, 'D': 0, 'F': 8}, 'samples_num1000000': {'I': 3, 'DIST': 4, 'D': 0, 'F': 1}}, 'error7': {'samples_num4000000': {'I': 18, 'DIST': 22, 'D': 1, 'F': 3}, 'samples_num500000': {'I': 1, 'DIST': 1, 'D': 0, 'F': 0}, 'samples_num100000': {'I': 0, 'DIST': 357, 'D': 357, 'F': 0}, 'samples_num3000000': {'I': 11, 'DIST': 12, 'D': 0, 'F': 1}, 'samples_num2000000': {'I': 11, 'DIST': 12, 'D': 0, 'F': 1}, 'samples_num1000000': {'I': 2, 'DIST': 2, 'D': 0, 'F': 0}}}}}}
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




        for key_length in key_length_vec:
            workbook = xlsxwriter.Workbook('./simulation_table{0}.xlsx'.format(key_length_vec[0]))
            worksheet = workbook.add_worksheet()
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




