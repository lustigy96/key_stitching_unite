#! /usr/bin/python
import numpy as np
import pandas as pd
import key_stitching_functinos as func
import os


def Probe(probe_len):
    path170 = "./samples/good_decoded_samples_probe170.txt"
    path230 = "./samples/good_decoded_samples_probe230.txt"
    if probe_len == 170:
        return [path170]
    elif probe_len == 230:
        return [path230]

if __name__ == "__main__":

    SIMULATION = True

    DIR_RESULT_PATH = "./results"
    DIR_PATH_REALCHANNEL = "/realChannel"


    try:
        os.mkdir(DIR_RESULT_PATH)
    except:
        pass

    try:
        os.mkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL)
    except:
        pass

    print "\n\n~~Start Gabi Algorithem...~~\n\n"

    hex_key_512="023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd"
    key=''.join(func.hex2bin_map[i] for i in hex_key_512)


    key_length_vec = [len(key)]
    probe_len_vec = [170,230]
    # megic_num_vec = [10, 30, 50]
    samples_num_vec = [100000, 500000, 1000000, 2000000, 3000000, 4000000, 5000000]
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

    error_vec = ["REAL"]

    tableResult = {}


    i=0
    for key_length in key_length_vec:
        KEY_LENGTH_PATH = "/key_length{0}".format(key_length)
        DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + KEY_LENGTH_PATH
        try:
            os.mkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + KEY_LENGTH_PATH)
        except:
            pass
        tableResult["key_length{0}".format(key_length)] = {}

        for probe_len in probe_len_vec:
            p_list = Probe(probe_len)

            SAMPLE_LEN_PATH = "/probe_len{0}".format(probe_len)

            DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + KEY_LENGTH_PATH + SAMPLE_LEN_PATH

            try:
                os.mkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + KEY_LENGTH_PATH + SAMPLE_LEN_PATH)
            except:
                pass
            tableResult["key_length{0}".format(key_length)]["probe_len{0}".format(probe_len)] = {}

            for window_size in window_size_vec:
                WINDOWS_SIZE_PATH = "/window_size{0}".format(window_size)
                try:
                    os.mkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + KEY_LENGTH_PATH + SAMPLE_LEN_PATH + WINDOWS_SIZE_PATH)
                except:
                    pass
                tableResult["key_length{0}".format(key_length)]["probe_len{0}".format(probe_len)]["window_size{0}".format(window_size)] = {}

                for error in error_vec:
                    ERROR_PATH = "/error{0}".format(error)
                    try:
                        os.mkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + KEY_LENGTH_PATH + SAMPLE_LEN_PATH + WINDOWS_SIZE_PATH + ERROR_PATH)
                    except:
                        pass
                    tableResult["key_length{0}".format(key_length)]["probe_len{0}".format(probe_len)][
                        "window_size{0}".format(window_size)]["error{0}".format(error)] = {}


                    start_samp = 0
                    result_dict = {}
                    for samples_num in samples_num_vec:
                        SAMPLE_NUM_PATH = "/samples_num{0}".format(samples_num)
                        try:
                            os.mkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + KEY_LENGTH_PATH + SAMPLE_LEN_PATH + WINDOWS_SIZE_PATH + ERROR_PATH + SAMPLE_NUM_PATH)
                        except:
                            pass
                        tableResult["key_length{0}".format(key_length)]["probe_len{0}".format(probe_len)][
                            "window_size{0}".format(window_size)]["error{0}".format(error)]["samples_num{0}".format(samples_num)] = {}




                        summryMy = open(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + KEY_LENGTH_PATH + SAMPLE_LEN_PATH + WINDOWS_SIZE_PATH + ERROR_PATH + SAMPLE_NUM_PATH + "/summryMy.txt", "w")

                        result_df, result_dict = func.build_samples_from_file(p_list=p_list, window_size=window_size,
                                                                              sample_start=start_samp,
                                                                              sample_end=samples_num,
                                                                              result_dict=result_dict)
                        start_samp = samples_num
                        common_samples_df = func.prune_samples_extended(result_df, min_count=-1, quantile=quantile)

                        all2PowerWindowArray_idx, shift_pointers_right_index, shift_pointers_right_index_left, shift_pointers_right_index_shift, shift_pointers_left_index, shift_pointers_left_index_right, shift_pointers_left_index_shift = \
                            func.build_shift_pointers_noDict(common_samples_df=common_samples_df,
                                                             stitch_shift_size=stitch_shift_size,
                                                             window_size=window_size)

                        retrieved_key = func.stitch_boris_noDict(common_samples_df=common_samples_df,
                                                                 all2PowerWindowArray_idx=all2PowerWindowArray_idx,
                                                                 shift_pointers_right_index=shift_pointers_right_index,
                                                                 shift_pointers_right_index_left=shift_pointers_right_index_left,
                                                                 shift_pointers_right_index_shift=shift_pointers_right_index_shift,
                                                                 shift_pointers_left_index=shift_pointers_left_index,
                                                                 shift_pointers_left_index_right=shift_pointers_left_index_right,
                                                                 shift_pointers_left_index_shift=shift_pointers_left_index_shift)

                        candidate_key = max(retrieved_key, key=len)

                        ## print results conclusion to file
                        string = "\nRESULT_NUMBER = {0}".format(i)
                        summryMy.write(string)
                        string = "\noriginal key(len={0}):\n".format(key_length) + key
                        summryMy.write(string)
                        string = "\ncandidate_key(len={0}):\n".format(len(candidate_key)) + candidate_key
                        summryMy.write(string)
                        string = "\nkey.find(candidate_key) = " + str(key.find(candidate_key))
                        summryMy.write(string)
                        conclusion, s1_match_indices = func.levenshtein_edit_dist(key, candidate_key)
                        string = "\nlevenshtein_edit_dist(key, candidate_key) = \n" + str(
                            (conclusion, s1_match_indices))
                        summryMy.write(string)
                        string = "\nSIMULATION = " + str(SIMULATION)
                        summryMy.write(string)
                        string = "\nsamples_num = " + str(samples_num) + \
                                 "\nresult_df = " + str(len(result_df)) + \
                                 "\ncommon_samples_df quantile = " + str(quantile) + \
                                 "\ncommon_samples_df = " + str(len(common_samples_df)) + \
                                 "\nstitch_shift_size = " + str(stitch_shift_size) + \
                                 "\nwindow_size = " + str(window_size) + \
                                 "\n"
                        summryMy.write(string)




                        dist = conclusion  # func.levenshtein_edit_dist(candidate_key,key, False)[0]
                        string = "\nDIST = " + str(dist['DIST']) + \
                                 "\nI = " + str(dist['I']) + \
                                 "\nD = " + str(dist['D']) + \
                                 "\nF = " + str(dist['F']) + \
                                 "\n"
                        summryMy.write(string)
                        summryMy.close()

                        tableResult["key_length{0}".format(key_length)]["probe_len{0}".format(probe_len)][
                            "window_size{0}".format(window_size)]["error{0}".format(error)]["samples_num{0}".format(samples_num)] = dist

                        tableFile = open(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + "/table.txt", "w")
                        tableFile.write(str(tableResult))
                        tableFile.close()















