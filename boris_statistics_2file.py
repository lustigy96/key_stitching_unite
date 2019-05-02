import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import os
import sys
from bitstring import BitArray

import operator as op
from functools import reduce

import key_stitching_functinos as func

if __name__ == "__main__":

    SIMULATION = False  # False -  this mean it will take samples from file
    GABI_SLOW = False
    MY_FAST = True

    SHIFT_POINTERS_METHOD = "position"  # "position"     # yael dont touch this..
    COMPRAE_GUBI_AND_MY = True  # yael dont touch this..
    ALLOW_CYCLES = True  # yael dont touch this..

    # hex_key_2048="023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e70f808182838485868788898a8b8c8d8e8909192939495969798999a9b9c9d9e91a0a1a2a3a4a5a6a7a8a9aaabacadaea1b0b1b2b3b4b5b6b7b8b9babbbcbdbeb1c0c1c2c3c4c5c6c7c8c9cacbcccdcec1"
    hex_key_500 = "023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd"
    key = ''.join(func.hex2bin_map[i] for i in hex_key_500)

    path = "./samples/key500_probe300_good_decoded_samples_486K.txt"
    path2 = "./samples/key500_probe300_good_decoded_samples_486KV2.txt"
    path3 = "./samples/key500_probe300_good_decoded_samples_170Ksamp.txt"

    try:
        os.mkdir("./results/")
    except:
        None

    print "\n\n~~Start Gabi Algorithem...~~\n\n"

    if SIMULATION:
        key_length_list = [512]
        sample_len_list = [50]  # [50, 60, 70, 80, 100]
        window_list = [15, 19]
        quantile_list = [0.5]
        num_constant_list = [100]
        stitch_list = [1]

        for bol in [True]:
            ALLOW_CYCLES = bol
            for key_length_value in key_length_list:
                for window_size_value in window_list:
                    for stitch_shift_size_value in stitch_list:
                        for sample_len_value in sample_len_list:
                            for num_constant_value in num_constant_list:
                                for quantile_value in quantile_list:

                                    cut_beginging = 0
                                    n = key_length = key_length_value
                                    window_size = window_size_value
                                    stitch_shift_size = stitch_shift_size_value
                                    quantile = quantile_value
                                    num_constant = num_constant_value

                                    # f_candidates = open("./results/candidates.txt", "w")
                                    # f_candidates2 = open("./results/candidates2.txt", "w")

                                    print "start simulation ..."
                                    key = func.init_key(n, 41)
                                    sample_len = sample_len_value
                                    flip_probability = 0.22  # (float)(110/500)
                                    delete_probability = 0.05  # (float)(20/500)
                                    insert_probability = 0.05  # (float)(20/500)
                                    num_samples = num_constant * (n - sample_len) * (sample_len - window_size)
                                    print "num_samples = {}".format(num_samples)
                                    result_df = func.build_samples(key, num_samples, sample_len, window_size,
                                                                   flip_probability, delete_probability,
                                                                   insert_probability, n)

                                    common_samples_df = func.prune_samples_extended(result_df, min_count=-1,
                                                                                    quantile=quantile)
                                    print "result_df = " + str(len(result_df))
                                    print "common_samples_df = " + str(len(common_samples_df))

                                    if MY_FAST:
                                        summryMy = open(
                                            "./results/summryMy_key={0}_allowCycle={1}_shiftPointersMethod={2}_windowSize={3}_simulation={4}.txt".format(
                                                n, ALLOW_CYCLES, SHIFT_POINTERS_METHOD, window_size, SIMULATION), "a+")
                                        if SHIFT_POINTERS_METHOD == "count":
                                            shift_pointers_Boris = func.build_shift_pointers_noorder(common_samples_df,
                                                                                                     stitch_shift_size,
                                                                                                     window_size,
                                                                                                     ALLOW_CYCLES)
                                        if SHIFT_POINTERS_METHOD == "position":
                                            shift_pointers_Boris = func.build_shift_pointers_position_better(
                                                common_samples_df, stitch_shift_size, window_size, ALLOW_CYCLES)

                                        if COMPRAE_GUBI_AND_MY:
                                            shift_pointers_Gabi = func.build_shift_pointers_gabi_pure(common_samples_df,
                                                                                                      stitch_shift_size)
                                            r = func.compareGabiAndMe(shift_pointers_Boris, shift_pointers_Gabi)
                                            if r == False:
                                                sys.exit(1)

                                        retrieved_key = func.stitch(common_samples_df, shift_pointers_Boris)
                                        candidate_key = max(retrieved_key, key=len)

                                        string = "\n\n\n\n~~~~~~~~~~~~~~~~~~~~~~\nMY_FAST = " + str(MY_FAST)
                                        print string
                                        summryMy.write(string)

                                        string = "\noriginal key(len={0}):\n".format(n) + key
                                        print string
                                        summryMy.write(string)

                                        string = "\ncandidate_key(len={0}):\n".format(
                                            len(candidate_key)) + candidate_key
                                        print string
                                        summryMy.write(string)
                                        string = "\nkey.find(candidate_key) = " + str(key.find(candidate_key))
                                        print string
                                        summryMy.write(string)

                                        string = "\nlevenshtein_edit_dist(key, candidate_key) = \n" + str(
                                            func.levenshtein_edit_dist(key, candidate_key))
                                        print string
                                        summryMy.write(string)

                                        # # print levenshtein_edit_dist(candidate_key, key, False)[0]
                                        # for cand in retrieved_key:
                                        #     if len(cand) > n / 3:
                                        #         f_candidates.write(cand)
                                        #         f_candidates.write("\n")
                                        # f_candidates.close()

                                        string = "\nSIMULATION = " + str(SIMULATION)
                                        print string
                                        summryMy.write(string)

                                        string = "\nsample_len = " + str(sample_len) + \
                                                 "\nflip_probability = " + str(flip_probability) + \
                                                 "\ndelete_probability = " + str(delete_probability) + \
                                                 "\ninsert_probability = " + str(insert_probability) + \
                                                 "\nnum_samples = " + str(num_samples)
                                        print string
                                        summryMy.write(string)

                                        string = "\nresult_df = " + str(len(result_df)) + \
                                                 "\ncommon_samples_df quantile = " + str(quantile) + \
                                                 "\ncommon_samples_df = " + str(len(common_samples_df)) + \
                                                 "\nstitch_shift_size = " + str(stitch_shift_size) + \
                                                 "\nnum_constant = " + str(num_constant) + \
                                                 "\nwindow_size = " + str(window_size) + \
                                                 "\nallowCycle = " + str(ALLOW_CYCLES)
                                        print string
                                        summryMy.write(string)
                                        summryMy.close()


    if not SIMULATION:

        window_list = [20, 30]
        quantile_list = [0.3, 0.4, 0.5]
        stitch_list = [1]

        for bol in [True]:  ## ALLOW GABI METHOD
            ALLOW_CYCLES = bol
            for window_size_value in window_list:
                for stitch_shift_size_value in stitch_list:
                    for quantile_value in quantile_list:

                        cut_beginging = 0
                        key_length = len(key)
                        n = key_length
                        window_size = window_size_value
                        stitch_shift_size = stitch_shift_size_value
                        quantile = quantile_value

                        # f_candidates = open("./results/candidates.txt", "w")
                        # f_candidates2 = open("./results/candidates2.txt", "w")

                        print "start real ..."
                        p_list = []
                        p_list.append(path)
                        # pathlist.append(path2)
                        result_df = func.build_samples_from_file(p_list=p_list, window_size=window_size, sample_start=0, sample_end=100000)

                        common_samples_df = func.prune_samples_extended(result_df, min_count=-1, quantile=quantile)
                        print "result_df = " + str(len(result_df))
                        print "common_samples_df = " + str(len(common_samples_df))

                        if MY_FAST:
                            if SHIFT_POINTERS_METHOD == "count":
                                shift_pointers_Boris = func.build_shift_pointers_noorder(common_samples_df,
                                                                                         stitch_shift_size, window_size,
                                                                                         ALLOW_CYCLES)
                            if SHIFT_POINTERS_METHOD == "position":
                                shift_pointers_Boris = func.build_shift_pointers_position_better(common_samples_df,
                                                                                                 stitch_shift_size,
                                                                                                 window_size,
                                                                                                 ALLOW_CYCLES)

                            if COMPRAE_GUBI_AND_MY:
                                shift_pointers_Gabi = func.build_shift_pointers_gabi_pure(common_samples_df,
                                                                                          stitch_shift_size)
                                r = func.compareGabiAndMe(shift_pointers_Boris, shift_pointers_Gabi)
                                if r==False:
                                    sys.exit(1)

                            retrieved_key = func.stitch(common_samples_df, shift_pointers_Boris)
                            candidate_key = max(retrieved_key, key=len)

                        string = "\n\n\n\n~~~~~~~~~~~~~~~~~~~~~~\nMY_FAST = " + str(MY_FAST)
                        print string
                        summryMy.write(string)

                        string = "\noriginal key(len={0}):\n".format(n) + key
                        print string
                        summryMy.write(string)

                        string = "\ncandidate_key(len={0}):\n".format(len(candidate_key)) + candidate_key
                        print string
                        summryMy.write(string)
                        string = "\nkey.find(candidate_key) = " + str(key.find(candidate_key))
                        print string
                        summryMy.write(string)

                        string = "\nlevenshtein_edit_dist(key, candidate_key) = \n" + str(
                            func.levenshtein_edit_dist(key, candidate_key))
                        print string
                        summryMy.write(string)

                        # # print levenshtein_edit_dist(candidate_key, key, False)[0]
                        # for cand in retrieved_key:
                        #     if len(cand) > n / 3:
                        #         f_candidates.write(cand)
                        #         f_candidates.write("\n")
                        # f_candidates.close()

                        string = "\nSIMULATION = " + str(SIMULATION)
                        print string
                        summryMy.write(string)

                        string = "\nresult_df = " + str(len(result_df)) + \
                                 "\ncommon_samples_df quantile = " + str(quantile) + \
                                 "\ncommon_samples_df = " + str(len(common_samples_df)) + \
                                 "\nstitch_shift_size = " + str(stitch_shift_size) + \
                                 "\nwindow_size = " + str(window_size) + \
                                 "\nallowCycle = " + str(ALLOW_CYCLES)
                        print string
                        summryMy.write(string)

                        summryMy.close()

