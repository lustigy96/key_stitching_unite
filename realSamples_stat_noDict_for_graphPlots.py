#! /usr/bin/python

import numpy as np
import pandas as pd
import key_stitching_functinos as func
import os

if __name__ == "__main__":

    SIMULATION = False
    ALLOW_CYCLES = False
    opposite = True
    regular = True
    try:
        os.mkdir("./results/")
    except:
        pass

    try:
        os.mkdir("./results/realChannel/")
    except:
        pass

    print "\n\n~~Start Gabi Algorithem ...~~\n\n"

    hex_key_512 = "023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd"
    hex_key_1024 = "023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f"
    hex_key_2048 = "023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e70f808182838485868788898a8b8c8d8e8909192939495969798999a9b9c9d9e91a0a1a2a3a4a5a6a7a8a9aaabacadaea1b0b1b2b3b4b5b6b7b8b9babbbcbdbeb1c0c1c2c3c4c5c6c7c8c9cacbcccdcec1"
    hex_key_4096 = "023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e70f808182838485868788898a8b8c8d8e8909192939495969798999a9b9c9d9e91a0a1a2a3a4a5a6a7a8a9aaabacadaea1b0b1b2b3b4b5b6b7b8b9babbbcbdbeb1c0c1c2c3c4c5c6c7c8c9cacbcccdcec1d0d1d2d3d4d5d6d7d8d9dadbdcddded1e0e1e2e3e4e5e6e7e8e9eaebecedeee1f0f1f2f3f4f5f6f7f8f91a1b1c1d1e1f123456789abcdef1dcba9876543215211815222936435057647178859299106113120127134141148155162169176183190197203210217224231239246253260267274281289296303310317324331301123581321345589144233377610987159725844181676510946177112865746368750251213931964183178115142298320401346269217830935245785702123456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd"

    key512 = ''.join(func.hex2bin_map[i] for i in hex_key_512)
    key1024 = ''.join(func.hex2bin_map[i] for i in hex_key_1024)
    key2048 = ''.join(func.hex2bin_map[i] for i in hex_key_2048)
    key4096 = ''.join(func.hex2bin_map[i] for i in hex_key_4096)

    key = key1024
    # path = "/root/newDecodedSamples/newD_probe300_2_115k_of_3.9M_removeTrash=15/good_decoded_samples.txt"
    path = "./new_1024_probe230/good_decoded_samples.txt"
    # path2 = "/root/newDecodedSamples/newD_probe230_5.1M_of_5.5M_removeTrash=15/good_decoded_samples.txt"
    # path2 = "./samples/good_decoded_samples_probe300_1.txt"
    # path2 = "./samples/key500_probe300_good_decoded_samples_486KV2.txt"
    # path3 = "./samples/key500_probe300_good_decoded_samples_170Ksamp.txt"
    p_list = [path]

    window_size_vec = [30, 20]  # each has its own graph
    quantile_vec = [0.6, 0.9, 0.8]  # each has its own graph
    samples_num_vec = [100000, 200000, 300000]  # bars section
    stitch_shift_size = 1
    key_length = n = len(key)
    window_size = None
    quantile = 0.8

    GRAPHS = "WINDOES"  # QUANTILE
    X = "samplesNumVec"
    f_data_path = "./results/realChannel/dataForGraph_Key={0}_Graphs={1}_x={2}_windowSize={3}_quantile={4}_opposite={5}.txt".format(
        key_length, GRAPHS, X, window_size, quantile, opposite)
    f_data = open(f_data_path, "a+")
    f_data.write(' '.join(map(str, window_size_vec)))  # f_data.write(' '.join(map(str,quantile_vec)))
    f_data.write('\n')
    f_data.write(' '.join(map(str, samples_num_vec)))
    f_data.write('\n')
    f_data.close()
    i = 1
    for window_size in window_size_vec:
        start_samp = 0
        result_dict = {}
        for samples_num in samples_num_vec:
            f_data = open(f_data_path, "a+")
            summryMy = open(
                "./results/realChannel/summryMy_keyLength={0}_windowSize={1}_quantile={2}_opposite{3}.txt".format(
                    key_length, window_size, quantile, opposite), "a+")

            result_df, result_dict = func.build_samples_from_file(p_list=p_list, window_size=window_size,
                                                                  sample_start=start_samp, sample_end=samples_num,
                                                                  result_dict=result_dict)
            start_samp = samples_num
            common_samples_df = func.prune_samples_extended(result_df, min_count=-1, quantile=quantile)

            if regular == True:
                all2PowerWindowArray_idx, shift_pointers_right_index, shift_pointers_right_index_left, shift_pointers_right_index_shift, shift_pointers_left_index, shift_pointers_left_index_right, shift_pointers_left_index_shift = \
                    func.build_shift_pointers_noDict(common_samples_df=common_samples_df,
                                                     stitch_shift_size=stitch_shift_size,
                                                     window_size=window_size)

                retrieved_key_regular = func.stitch_boris_noDict(common_samples_df=common_samples_df,
                                                                 all2PowerWindowArray_idx=all2PowerWindowArray_idx,
                                                                 shift_pointers_right_index=shift_pointers_right_index,
                                                                 shift_pointers_right_index_left=shift_pointers_right_index_left,
                                                                 shift_pointers_right_index_shift=shift_pointers_right_index_shift,
                                                                 shift_pointers_left_index=shift_pointers_left_index,
                                                                 shift_pointers_left_index_right=shift_pointers_left_index_right,
                                                                 shift_pointers_left_index_shift=shift_pointers_left_index_shift)
            if opposite == True:
                all2PowerWindowArray_idx, shift_pointers_right_index, shift_pointers_right_index_left, shift_pointers_right_index_shift, shift_pointers_left_index, shift_pointers_left_index_right, shift_pointers_left_index_shift = \
                    func.build_shift_pointers_noDict_opposite(common_samples_df=common_samples_df,
                                                              stitch_shift_size=stitch_shift_size,
                                                              window_size=window_size)

                retrieved_key_opposite = func.stitch_boris_noDict_opposite(common_samples_df=common_samples_df,
                                                                           all2PowerWindowArray_idx=all2PowerWindowArray_idx,
                                                                           shift_pointers_right_index=shift_pointers_right_index,
                                                                           shift_pointers_right_index_left=shift_pointers_right_index_left,
                                                                           shift_pointers_right_index_shift=shift_pointers_right_index_shift,
                                                                           shift_pointers_left_index=shift_pointers_left_index,
                                                                           shift_pointers_left_index_right=shift_pointers_left_index_right,
                                                                           shift_pointers_left_index_shift=shift_pointers_left_index_shift)

            candidate_key_regular = max(retrieved_key_regular, key=len)
            candidate_key_opposite = max(retrieved_key_opposite, key=len)

            ## print results conclusion to file
            string = "\nRESULT_NUMBER = {0}".format(i)
            summryMy.write(string)
            string = "\noriginal key(len={0}):\n".format(key_length) + key
            summryMy.write(string)
            string = "\n\ncandidate_key_regular(len={0}):\n".format(len(candidate_key_regular)) + candidate_key_regular
            summryMy.write(string)
            string = "\nkey.find(candidate_key_regular) = " + str(key.find(candidate_key_regular))
            summryMy.write(string)
            conclusion, s1_match_indices = func.levenshtein_edit_dist(key, candidate_key_regular)
            string = "\nlevenshtein_edit_dist(key, candidate_key_regular) = \n" + str((conclusion, s1_match_indices))
            summryMy.write(string)

            string = "\ncandidate_key_opposite(len={0}):\n".format(len(candidate_key_opposite)) + candidate_key_opposite
            summryMy.write(string)
            string = "\nkey.find(candidate_key_opposite) = " + str(key.find(candidate_key_opposite))
            summryMy.write(string)
            conclusion, s1_match_indices = func.levenshtein_edit_dist(key, candidate_key_opposite)
            string = "\nlevenshtein_edit_dist(key, candidate_key_opposite) = \n" + str((conclusion, s1_match_indices))
            summryMy.write(string)

            string = "\nSIMULATION = " + str(SIMULATION)
            summryMy.write(string)
            string = "\nsamples_num = " + str(samples_num) + \
                     "\nresult_df = " + str(len(result_df)) + \
                     "\ncommon_samples_df quantile = " + str(quantile) + \
                     "\ncommon_samples_df = " + str(len(common_samples_df)) + \
                     "\nstitch_shift_size = " + str(stitch_shift_size) + \
                     "\nwindow_size = " + str(window_size) + \
                     "\nallowCycle = " + str(ALLOW_CYCLES) + \
                     "\n"
            summryMy.write(string)
            summryMy.close()

            dist = conclusion  # func.levenshtein_edit_dist(candidate_key,key, False)[0]
            f_data.write(
                str(dist['DIST']) + " " + str(dist['I']) + " " + str(dist['D']) + " " + str(dist['F']) + " " + str(
                    len(candidate_key_regular)) + "\n")
            f_data.close()
            i += 1









