import numpy as np
import pandas as pd
import key_stitching_functinos as func
import os







if __name__ == "__main__":


    try:
        os.mkdir("./results/")
    except:
        None

    print "\n\n~~Start Gabi Algorithem...~~\n\n"


    hex_key_500="023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd"
    key=''.join(func.hex2bin_map[i] for i in hex_key_500)
    path = "./samples/key500_probe300_good_decoded_samples_486K.txt"



    window_size_vec=[20,30] #each has its own graph
    quantile_vec=[0.3,0.5,0.7] #each has its own graph
    samples_num_vec=[1000]#[1000, 200000, 300000] #bars section
    start_samp=0
    result_dict={}
    ALLOW_CYCLES = True
    stitch_shift_size = 1
    key_length = n = len(key)
    window_size = 30
    SIMULATION = False


    f_data=open("./results/data.txt","w")

    f_data.write(' '.join(map(str,quantile_vec)))
    f_data.write('\n')
    f_data.write(' '.join(map(str,samples_num_vec)))
    f_data.write('\n')
    for quantile in quantile_vec:
        for samples_num in samples_num_vec:
            summryMy = open("./results/summryMy_keyLength={0}_allowCycle={1}_shiftPointersMethod=GabiOptimized_windowSize={2}_simulation={3}.txt".format(key_length, ALLOW_CYCLES, window_size, SIMULATION), "a+")

            print "start real ..."
            p_list = []
            p_list.append(path)
            result_df, result_dict = func.build_samples_from_file(p_list=p_list, window_size=window_size, sample_start=start_samp, sample_end=samples_num, result_dict=result_dict)
            common_samples_df = func.prune_samples_extended(result_df, min_count=-1, quantile=quantile)
            shift_pointers_Boris, all2PowerWindowArray, all2PowerWindowArray_idx, orderArrayMaxToMin = func.build_shift_pointers_position_better(common_samples_df, stitch_shift_size, window_size, ALLOW_CYCLES)

            retrieved_key = func.stitch_boris(common_samples_df, shift_pointers_Boris, all2PowerWindowArray_idx, allowCycle=ALLOW_CYCLES, key_length=key_length)
            candidate_key = max(retrieved_key, key=len)

            ## print results conclusion to file
            string = "\n\n\n\n~~~~~~~~~~~~~~~~~~~~~~\nResults ~~~~~~~~ "
            summryMy.write(string)
            string = "\noriginal key(len={0}):\n".format(n) + key
            summryMy.write(string)
            string = "\ncandidate_key(len={0}):\n".format(len(candidate_key)) + candidate_key
            summryMy.write(string)
            string = "\nkey.find(candidate_key) = " + str(key.find(candidate_key))
            summryMy.write(string)
            string = "\nlevenshtein_edit_dist(key, candidate_key) = \n" + str(func.levenshtein_edit_dist(key, candidate_key))
            summryMy.write(string)
            string = "\nSIMULATION = " + str(SIMULATION)
            summryMy.write(string)
            string = "\nresult_df = " + str(len(result_df)) + \
                     "\ncommon_samples_df quantile = " + str(quantile) + \
                     "\ncommon_samples_df = " + str(len(common_samples_df)) + \
                     "\nstitch_shift_size = " + str(stitch_shift_size) + \
                     "\nwindow_size = " + str(window_size) + \
                     "\nallowCycle = " + str(ALLOW_CYCLES)
            summryMy.write(string)
            summryMy.close()


            dist = func.levenshtein_edit_dist(candidate_key,key, False)[0]
            f_data.write(str(dist['DIST'])+" "+str(dist['I'])+" "+str(dist['D'])+" "+str(dist['F'])+" "+str(len(key)-len(candidate_key))+"\n")

    f_data.close()





