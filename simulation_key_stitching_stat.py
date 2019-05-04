import numpy as np
import pandas as pd
import key_stitching_functinos as func
import os







if __name__ == "__main__":

    SIMULATION = True
    ALLOW_CYCLES = False
    CASE = 2 ## 1=error15%(5,5,5)  2=error30%(22,5,5) 3=error20%(10,5,5)
    try:
        os.mkdir("./results/")
    except:
        None

    try:
        os.mkdir("./results/simulation/")
    except:
        None

    print "\n\n~~Start Gabi Algorithem...~~\n\n"





    key_length_vec = [512,1024,2048]
    sample_len_vec = [31,40,50]  # [50, 60, 70, 80, 100]
    megic_num_vec = [10, 25, 50, 100, 150]
    stitch_vec = [1]
    window_size_vec=[30,20] #each has its own graph
    quantile_vec=[0.5] #each has its own graph

    stitch_shift_size = 1
    window_size = 20
    quantile = 0.5
    sample_len = 50


    if CASE==1:
        flip_probability = 0.05
        delete_probability = 0.05
        insert_probability = 0.05
        f_data = open("./results/simulation/dataForGraph_ErrorProbabilty=5%_Graphs=keyLength_X=megicNumVec.txt", "a+")


    if CASE==2:
        flip_probability = 0.22
        delete_probability = 0.05
        insert_probability = 0.05
        f_data = open("./results/simulation/dataForGraph_ErrorProbabilty=20%_Graphs=keyLength_X=megicNumVec.txt", "a+")

    if CASE==3:
        flip_probability = 0.1
        delete_probability = 0.05
        insert_probability = 0.05
        f_data = open("./results/simulation/dataForGraph_ErrorProbabilty=10%_Graphs=keyLength_X=megicNumVec.txt", "a+")

    f_data.write(' '.join(map(str,key_length_vec)))
    f_data.write('\n')
    f_data.write(' '.join(map(str,megic_num_vec)))
    f_data.write('\n')
    f_data.close()

    i=0
    for key_length in key_length_vec:
        start_samp = 0
        result_dict = {}
        key = func.init_key(key_length, 41)
        for megic_num in megic_num_vec:
            if CASE == 1:
                f_data = open("./results/simulation/dataForGraph_ErrorProbabilty=5%_Graphs=keyLength_X=megicNumVec.txt","a+")
            if CASE == 2:
                f_data = open("./results/simulation/dataForGraph_ErrorProbabilty=20%_Graphs=keyLength_X=megicNumVec.txt","a+")
            if CASE == 3:
                f_data = open("./results/simulation/dataForGraph_ErrorProbabilty=10%_Graphs=keyLength_X=megicNumVec.txt","a+")
            summryMy = open("./results/simulation/summryMy_keyLength={0}_allowCycle={1}_shiftPointersMethod=GabiOptimized_windowSize={2}_simulation={3}.txt".format(key_length, ALLOW_CYCLES, window_size, SIMULATION), "a+")

            samples_num = megic_num * (key_length - sample_len) * (sample_len - window_size)
            result_df, result_dict = func.build_samples_better(key=key, sample_start=sample_start, num_samples=samples_num, sample_len=sample_len, window_size=window_size, flip_probability=flip_probability, delete_probability=delete_probability, insert_probability=insert_probability, result_dict=result_dict)
            sample_start = samples_num
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
            string = "\nmegic_num = " + str(megic_num) + \
                     "\nsample_len = " + str(sample_len) + \
                     "\nsamples_num = megic_num * (key_length - sample_len) * (sample_len - window_size) = " + str(samples_num) + \
                     "\nflip_probability = " + str(flip_probability) + \
                     "\ninsert_probability = " + str(insert_probability) + \
                     "\ndelete_probability = " + str(delete_probability) + \
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





