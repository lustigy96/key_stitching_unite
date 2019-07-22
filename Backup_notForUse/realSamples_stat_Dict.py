#! /usr/bin/python
import numpy as np
import pandas as pd
import key_stitching_functinos as func
import os







if __name__ == "__main__":

    SIMULATION = False
    ALLOW_CYCLES = False
    try:
        os.mkdir("./results/")
    except:
        None

    try:
        os.mkdir("./results/realChannel/")
    except:
        None

    print "\n\n~~Start Gabi Algorithem ...~~\n\n"

    hex_key_512 = "023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd"
    hex_key_1024 = "023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f"
    hex_key_2048 = "023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e70f808182838485868788898a8b8c8d8e8909192939495969798999a9b9c9d9e91a0a1a2a3a4a5a6a7a8a9aaabacadaea1b0b1b2b3b4b5b6b7b8b9babbbcbdbeb1c0c1c2c3c4c5c6c7c8c9cacbcccdcec1"
    hex_key_4096 = "023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e70f808182838485868788898a8b8c8d8e8909192939495969798999a9b9c9d9e91a0a1a2a3a4a5a6a7a8a9aaabacadaea1b0b1b2b3b4b5b6b7b8b9babbbcbdbeb1c0c1c2c3c4c5c6c7c8c9cacbcccdcec1d0d1d2d3d4d5d6d7d8d9dadbdcddded1e0e1e2e3e4e5e6e7e8e9eaebecedeee1f0f1f2f3f4f5f6f7f8f91a1b1c1d1e1f123456789abcdef1dcba9876543215211815222936435057647178859299106113120127134141148155162169176183190197203210217224231239246253260267274281289296303310317324331301123581321345589144233377610987159725844181676510946177112865746368750251213931964183178115142298320401346269217830935245785702123456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd"

    key512 = ''.join(func.hex2bin_map[i] for i in hex_key_512)
    key1024 = ''.join(func.hex2bin_map[i] for i in hex_key_1024)
    key2048 = ''.join(func.hex2bin_map[i] for i in hex_key_2048)
    key4096 = ''.join(func.hex2bin_map[i] for i in hex_key_4096)

    key = key512


    path = "./samples/key500_probe300_good_decoded_samples_486K.txt"
    path2 = "./samples/key500_probe300_good_decoded_samples_486KV2.txt"
    path3 = "./samples/key500_probe300_good_decoded_samples_170Ksamp.txt"


    window_size_vec=[30, 20] #each has its own graph
    quantile_vec=[0.5, 0.8, 0.9] #each has its own graph
    samples_num_vec=[100000, 300000 , 600000, 800000, 1000000, 2000000] #bars section
    stitch_shift_size = 1
    key_length = n = len(key)
    window_size = 30
    # quantile = 0.5

    GRAPHS = "QUANTILE" #"WINDOES" # QUANTILE
    X= "samplesNumVec"
    f_data_path = "./results/realChannel/dataForGraph_Key={0}_Graphs={1}_x={2}_windowSize={3}_quantile={4}.txt".format(key_length,GRAPHS,X, window_size,quantile)
    f_data = open(f_data_path,"a+")
    f_data.write(' '.join(map(str,quantile_vec)))
    f_data.write('\n')
    f_data.write(' '.join(map(str,samples_num_vec)))
    f_data.write('\n')
    f_data.close()
    i = 1
    for quantile in quantile_vec:
        start_samp = 0
        result_dict = {}
        for samples_num in samples_num_vec:
            f_data = open(f_data_path, "a+")
            summryMy = open("./results/realChannel/summryMy_keyLength={0}_windowSize={1}_quantile={2}.txt".format(key_length,  window_size,quantile), "a+")

            p_list = [path, path2, path3]
            result_df, result_dict = func.build_samples_from_file(p_list=p_list, window_size=window_size, sample_start=start_samp, sample_end=samples_num, result_dict=result_dict)
            start_samp = samples_num
            common_samples_df = func.prune_samples_extended(result_df, min_count=-1, quantile=quantile)
            shift_pointers_Boris, all2PowerWindowArray, all2PowerWindowArray_idx, orderArrayMaxToMin = func.build_shift_pointers_position_better(common_samples_df, stitch_shift_size, window_size, ALLOW_CYCLES)

            retrieved_key = func.stitch_boris(common_samples_df, shift_pointers_Boris, all2PowerWindowArray_idx, allowCycle=ALLOW_CYCLES, key_length=key_length)
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
            string = "\nlevenshtein_edit_dist(key, candidate_key) = \n" + str((conclusion, s1_match_indices))
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

            dist = conclusion #func.levenshtein_edit_dist(candidate_key,key, False)[0]
            f_data.write(str(dist['DIST'])+" "+str(dist['I'])+" "+str(dist['D'])+" "+str(dist['F'])+" "+str(len(candidate_key))+"\n")
            f_data.close()
            i+=1





