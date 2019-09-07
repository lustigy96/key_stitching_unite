#! /usr/bin/python
import numpy as np
import pandas as pd
import key_stitching_functinos as func
import os
import xlsxwriter


def Probe(probe_len, codeName):
    paths = {
        "Haswell":
            {
                180: ["./samples/Haswell/Haswell/work/180/good_decoded_samples.txt"],
                190: ["./samples/Haswell/Haswell/work/190/good_decoded_samples.txt"],
                230: ["./samples/Haswell/Haswell/work/230/good_decoded_samples_v1.txt",
                      "./samples/Haswell/Haswell/work/230/good_decoded_samples_v2.txt",
                      "./samples/Haswell/Haswell/work/230/good_decoded_samples_v3.txt"],
                260: ["./samples/Haswell/Haswell/work/230/good_decoded_samples_v1.txt",
                      "./samples/Haswell/Haswell/work/230/good_decoded_samples_v3.txt"],

                400: ["./samples/Haswell/Haswell/work/400/good_decoded_samples.txt"],
                550: ["./samples/Haswell/Haswell/work/550/good_decoded_samples.txt"],
            },
        "CoffeeLake":
            {
                130: ["./samples/CoffeeLake/130/good_decoded_samples.txt"],
                140: ["./samples/CoffeeLake/140/good_decoded_samples.txt"],
                150: ["./samples/CoffeeLake/150/good_decoded_samples.txt"],
                160: ["./samples/CoffeeLake/160/good_decoded_samples.txt"],
                170: ["./samples/CoffeeLake/170/good_decoded_samples.txt"],
                180: ["./samples/CoffeeLake/180/good_decoded_samples.txt"],
                190: ["./samples/CoffeeLake/190/good_decoded_samples.txt"],
                200: ["./samples/CoffeeLake/200/good_decoded_samples.txt"],
                230: ["./samples/CoffeeLake/230/good_decoded_samples.txt"],
                260: ["./samples/CoffeeLake/260/good_decoded_samples.txt"],
                300: ["./samples/CoffeeLake/300/good_decoded_samples.txt"],
                350: ["./samples/CoffeeLake/350/good_decoded_samples.txt"],
                400: ["./samples/CoffeeLake/400/good_decoded_samples.txt"],
                550: ["./samples/CoffeeLake/550/good_decoded_samples.txt"],
                700: ["./samples/CoffeeLake/700/good_decoded_samples.txt"],
            },
        "SkyLake":
            {
                180: [],
                230: ["./samples/SkyLake/probe230/good_decoded_samples_v0.txt"],
                300: [],
            },
    }
    return paths[codeName][probe_len]

def Opposite(common_samples_df, stitch_shift_size, window_size):
    all2PowerWindowArray_idx, shift_pointers_right_index, shift_pointers_right_index_left, shift_pointers_right_index_shift, shift_pointers_left_index, shift_pointers_left_index_right, shift_pointers_left_index_shift = \
        func.build_shift_pointers_noDict_opposite(common_samples_df=common_samples_df,
                                                  stitch_shift_size=stitch_shift_size,
                                                  window_size=window_size)
    retrieved_key = func.stitch_boris_noDict_opposite(common_samples_df=common_samples_df,
                                                      all2PowerWindowArray_idx=all2PowerWindowArray_idx,
                                                      shift_pointers_right_index=shift_pointers_right_index,
                                                      shift_pointers_right_index_left=shift_pointers_right_index_left,
                                                      shift_pointers_right_index_shift=shift_pointers_right_index_shift,
                                                      shift_pointers_left_index=shift_pointers_left_index,
                                                      shift_pointers_left_index_right=shift_pointers_left_index_right,
                                                      shift_pointers_left_index_shift=shift_pointers_left_index_shift)
    return retrieved_key

def notOpposite(common_samples_df, stitch_shift_size, window_size):
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
    return retrieved_key

methodFunDict ={
    "Opposite" : Opposite,
    "notOpposite": notOpposite
}



def TryMkdir(path):
    try:
        os.mkdir(path)
    except:
        pass


def PrintToSummryFile(file, key, key_length, candidate_key, samples_num, result_df, quantile, common_samples_df,
                      stitch_shift_size, window_size, conclusion, s1_match_indices):
    ## print results conclusion to file
    string = "\nRESULT_NUMBER = {0}".format(i)
    file.write(string)
    string = "\noriginal key(len={0}):\n".format(key_length) + key
    file.write(string)
    string = "\ncandidate_key(len={0}):\n".format(len(candidate_key)) + candidate_key
    file.write(string)
    string = "\nkey.find(candidate_key) = " + str(key.find(candidate_key))
    file.write(string)
    #conclusion, s1_match_indices = func.levenshtein_edit_dist(key, candidate_key)
    string = "\nlevenshtein_edit_dist(key, candidate_key) = \n" + str(
        (conclusion, s1_match_indices))
    file.write(string)
    string = "\nsamples_num = " + str(samples_num) + \
             "\nresult_df = " + str(len(result_df)) + \
             "\ncommon_samples_df quantile = " + str(quantile) + \
             "\ncommon_samples_df = " + str(len(common_samples_df)) + \
             "\nstitch_shift_size = " + str(stitch_shift_size) + \
             "\nwindow_size = " + str(window_size) + \
             "\n"
    file.write(string)

    string = "\nDIST = " + str(conclusion['DIST']) + \
             "\nI = " + str(conclusion['I']) + \
             "\nD = " + str(conclusion['D']) + \
             "\nF = " + str(conclusion['F'])
    file.write(string)
    return conclusion












#------------------------------------------------if __name__ == "__main__":----------------------------------------------------------------------

DIR_RESULT_PATH = "./results"
DIR_PATH_REALCHANNEL = "/realChannel"
PRINT_RETRIVED_KESYS = True
SIZE_OF_RETRIVED_KESYS_TO_PRINT = 0.995

TryMkdir(DIR_RESULT_PATH)
TryMkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL)

print "\n\n~~Start SFS Algorithem...~~\n\n"

hex_key_2048 = "40554dc4edd210b27e4be5d4d6dcde0f3ab8199730db8a5cf3f3d1617d956cd7dfa0b1e7f82f0b0949d67f7b2b3f84e62537d41eb0142aaf1f84aa6d74b1e0aa2bf82f84298e6d9f6aa580c75905bda8508aad6b73f75862246a7aebe964d543fa05b455b58a3a0f301ab9d9f4232a82e5aaed1303514109f0b4526eb5706c1d3c231e9bd9c96f647774fc923686f17b8707035db6b3f16163154c1d11276540ec776b341fe292def59bcfe161869fae2dc04de17603ae012a3b22d611a3643414e7eff365c8bd3b35323f56759dc6a9dd7704f5d760deb29e8bbd50586b8df7ee9c33d6b6abf9b625635b9db15360c5eae2b89dc4ff443722e5e6b06f71e930"

key2048 = ''.join(func.hex2bin_map[i] for i in hex_key_2048)

probe_len_vec = [150,160,170,180,190, 200,230,260, 300,350, 400,550, 700]  # [180,190,230,260,400,550]
window_size_vec = [30]
low = 50000
samples_num_vec = range(50000, 700001, low)
med = 10000
high = 2000
Fhigh = 500
quantile_vec = [0.9, 0.6]  # each has
method_vec = ["notOpposite", "Opposite"]

stitch_shift_size = 1

tableResult = {}

i = 0
codeName = "CoffeeLake" # ["Haswell"]  # ["SandyBrige", "Haswell", "CoffeeLake","SkyLake"]

CODE_NAME_PATH = "/cpuName_{0}".format(codeName)
TryMkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH)
tableResult["cpuName_{0}".format(codeName)] = {}

key = key2048
key_length = len(key2048)
KEY_LENGTH_PATH = "/key_length{0}".format(key_length)
TryMkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH)
tableResult["cpuName_{0}".format(codeName)]["key_length{0}".format(key_length)] = {}

for window_size in window_size_vec:
    WINDOWS_SIZE_PATH = "/window_size{0}".format(window_size)
    TryMkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH +
             WINDOWS_SIZE_PATH)
    tableResult["cpuName_{0}".format(codeName)][
        "key_length{0}".format(key_length)][
        "window_size{0}".format(window_size)] = {}

    workbook = xlsxwriter.Workbook(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH +
                                   '/table{0}_window_size{1}.xlsx'
                                   .format(key_length, window_size))
    worksheet = workbook.add_worksheet()

    r = -4
    for quantile in quantile_vec:
        r += 4
        QUANTILE_NUM_PATH = "/quantile{0}".format(quantile)
        TryMkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH +
                 WINDOWS_SIZE_PATH +
                 QUANTILE_NUM_PATH)
        tableResult["cpuName_{0}".format(codeName)][
            "key_length{0}".format(key_length)][
            "window_size{0}".format(window_size)]["quantile{0}".format(quantile)] = {}

        workbookQ = xlsxwriter.Workbook(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH + QUANTILE_NUM_PATH +
                                       '/table{0}_window_size{1}_q{2}.xlsx'
                                       .format(key_length, window_size,quantile))
        worksheetQ = workbookQ.add_worksheet()

        c = -2

        for probe_len in probe_len_vec:
            c += 2
            p_list = Probe(probe_len=probe_len, codeName=codeName)

            SAMPLE_LEN_PATH = "/probe_len{0}".format(probe_len)

            TryMkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH +
                     WINDOWS_SIZE_PATH +
                     QUANTILE_NUM_PATH +
                     SAMPLE_LEN_PATH)

            tableResult["cpuName_{0}".format(codeName)][
                "key_length{0}".format(key_length)][
                "window_size{0}".format(window_size)][
                "quantile{0}".format(quantile)][
                "probe_len{0}".format(probe_len)] = {}

            OK1 = False

            result_dict = {}
            sample_start = 0
            for s_idx, samples_num in enumerate(samples_num_vec, 0):
                if OK1:
                    break
                result_df, result_dict = func.build_samples_from_file(p_list=p_list,
                                                                      window_size=window_size,
                                                                      sample_start=sample_start,
                                                                      sample_end=samples_num,
                                                                      result_dict=result_dict)
                sample_start = samples_num
                common_samples_df = func.prune_samples_extended(result_df, min_count=-1, quantile=quantile)

                tmpOk = {}
                dist = {}
                retrieved_key = {}
                candidate_key = {}
                s1_match_indices = {}
                for method in method_vec:
                    methodFun = methodFunDict[method]
                    retrieved_key[method] = methodFun(common_samples_df, stitch_shift_size,
                                                       window_size)

                    candidate_key[method] = max(retrieved_key[method], key=len)
                    dist[method], s1_match_indices[method] = func.levenshtein_edit_dist(key, candidate_key[method])

                    tmpOk[method] = "BAD"
                    if dist[method]['DIST'] < 25:
                        if dist[method]['DIST'] - dist[method]['I'] <= 10 \
                                and candidate_key[method][:5] == "00000":
                            tmpOk[method] = "GOOD"
                            OK1 = True
                        elif dist[method]['DIST'] - dist[method]['I'] <= 10 \
                                and candidate_key[method][:-5] == "00000":
                            tmpOk[method] = "GOOD"
                            OK1 = True
                        elif dist[method]['DIST'] <= 10:
                            tmpOk[method] = "GOOD"
                            OK1 = True

                if not OK1:
                    SAMPLE_NUM_PATH = "/samples_num{0}".format(samples_num)
                    TryMkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH +
                             WINDOWS_SIZE_PATH +
                             QUANTILE_NUM_PATH +
                             SAMPLE_LEN_PATH +
                             SAMPLE_NUM_PATH)

                    tableResult["cpuName_{0}".format(codeName)][
                        "key_length{0}".format(key_length)][
                        "window_size{0}".format(window_size)][
                        "quantile{0}".format(quantile)][
                        "probe_len{0}".format(probe_len)][
                        "samples_num{0}".format(samples_num)] = {}

                    tmpC = c
                    for method in method_vec:
                        METHOD_PATH = "/{0}".format(method)
                        TryMkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH +
                                 WINDOWS_SIZE_PATH +
                                 QUANTILE_NUM_PATH +
                                 SAMPLE_LEN_PATH +
                                 SAMPLE_NUM_PATH +
                                 METHOD_PATH)

                        tableResult["cpuName_{0}".format(codeName)][
                            "key_length{0}".format(key_length)][
                            "window_size{0}".format(window_size)][
                            "quantile{0}".format(quantile)][
                            "probe_len{0}".format(probe_len)][
                            "samples_num{0}".format(samples_num)]["{0}".format(method)] = dist[method]

                        summryMy = open(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH +
                                        WINDOWS_SIZE_PATH +
                                        QUANTILE_NUM_PATH +
                                        SAMPLE_LEN_PATH +
                                        SAMPLE_NUM_PATH +
                                        METHOD_PATH + "/summryMy.txt", "w")

                        if PRINT_RETRIVED_KESYS:
                            retrievedKeysFile = open(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH +
                                                     KEY_LENGTH_PATH +
                                                     WINDOWS_SIZE_PATH +
                                                     QUANTILE_NUM_PATH +
                                                     SAMPLE_LEN_PATH +
                                                     SAMPLE_NUM_PATH +
                                                     METHOD_PATH + "/retrievedKeys.txt", "w")

                            for cankey in retrieved_key[method]:
                                if len(cankey) > SIZE_OF_RETRIVED_KESYS_TO_PRINT * len(key):
                                    retrievedKeysFile.write(cankey)
                                    retrievedKeysFile.write("\n")
                            retrievedKeysFile.close()

                        PrintToSummryFile(summryMy, key, key_length, candidate_key[method], samples_num, result_df,
                                          quantile, common_samples_df, stitch_shift_size, window_size, dist[method], s1_match_indices[method])

                        string = "\nDIST-INSERTION = " + str(dist[method]['DIST'] - dist[method]['I'])
                        summryMy.write(string)
                        summryMy.close()

                        dist[method]['DIST - INSERTIONS'] = dist[method]['DIST'] - dist[method]['I']

                        #---------------------------------------------------
                        worksheetQ.write(0, tmpC, int(dist[method]['DIST']))
                        worksheetQ.write(1, tmpC, str(dist[method]))
                        worksheetQ.write(2, tmpC, tmpOk[method])
                        worksheetQ.write(3, tmpC, int(samples_num))

                        #-----------------------------------------------------
                        worksheet.write(r, tmpC, int(dist[method]['DIST']))
                        worksheet.write(r + 1, tmpC, str(dist[method]))
                        worksheet.write(r + 2, tmpC, tmpOk[method])
                        worksheet.write(r + 3, tmpC, int(samples_num))
                        tmpC += 1

                        tableFileP = open(DIR_RESULT_PATH +
                                          DIR_PATH_REALCHANNEL +
                                          CODE_NAME_PATH +
                                          KEY_LENGTH_PATH +
                                          WINDOWS_SIZE_PATH +
                                          QUANTILE_NUM_PATH +
                                          "/real{0}_W{1}_Q{2}_probe{3}.json".format(key_length, window_size, quantile,
                                                                                    probe_len),
                                          "w")
                        tableFileP.write(
                            str(tableResult["cpuName_{0}".format(codeName)][
                                    "key_length{0}".format(key_length)][
                                    "window_size{0}".format(window_size)][
                                    "quantile{0}".format(quantile)][
                                    "probe_len{0}".format(probe_len)])
                        )
                        tableFileP.close()

                        tableFileQ = open(DIR_RESULT_PATH +
                                          DIR_PATH_REALCHANNEL +
                                          CODE_NAME_PATH +
                                          KEY_LENGTH_PATH +
                                          WINDOWS_SIZE_PATH +
                                          "/real{0}_W{1}_Q{2}.json".format(key_length, window_size, quantile),
                                          "w")
                        tableFileQ.write(str(tableResult["cpuName_{0}".format(codeName)][
                                                 "key_length{0}".format(key_length)][
                                                 "window_size{0}".format(window_size)][
                                                 "quantile{0}".format(quantile)]))
                        tableFileQ.close()

                        tableFile = open(DIR_RESULT_PATH +
                                         DIR_PATH_REALCHANNEL +
                                         "/real{0}.json".format(key_length),
                                         "w")
                        tableFile.write(str(tableResult))
                        tableFile.close()



                elif OK1:
                    OK2 = False
                    startM = samples_num_vec[s_idx - 1] if s_idx != 0 else med
                    endM = samples_num
                    vecM = range(startM, endM + med, med)

                    result_dict2 = {}
                    sample_start2 = 0
                    for sM_idx, samples_numM in enumerate(vecM, 0):
                        if OK2: break

                        result_df, result_dict2 = func.build_samples_from_file(p_list=p_list,
                                                                               window_size=window_size,
                                                                               sample_start=sample_start2,
                                                                               sample_end=samples_numM,
                                                                               result_dict=result_dict2)
                        common_samples_df = func.prune_samples_extended(result_df, min_count=-1, quantile=quantile)
                        sample_start2 = samples_numM
                        tmpOk2 = {}
                        dist2 = {}
                        retrieved_key2 = {}
                        candidate_key2 = {}
                        s1_match_indices2 = {}
                        for method in method_vec:
                            if tmpOk[method] == "BAD":
                                tmpOk2[method] = tmpOk[method]
                                dist2[method] = dist[method]
                                candidate_key2[method] = candidate_key[method]
                                retrieved_key2[method] = retrieved_key[method]
                                s1_match_indices2[method] = s1_match_indices[method]
                                continue

                            methodFun = methodFunDict[method]
                            retrieved_key2[method] = methodFun(common_samples_df, stitch_shift_size,
                                                                     window_size)

                            candidate_key2[method] = max(retrieved_key2[method], key=len)
                            dist2[method], s1_match_indices2[method] = func.levenshtein_edit_dist(key,
                                                                                         candidate_key2[method])

                            tmpOk2[method] = "BAD"
                            if dist2[method]['DIST'] < 25:
                                if dist2[method]['DIST'] - dist2[method]['I'] <= 10 and \
                                        candidate_key2[method][:5] == "00000":
                                    tmpOk2[method] = "GOOD"
                                    OK2 = True
                                elif dist2[method]['DIST'] - dist2[method]['I'] <= 10 and \
                                        candidate_key2[method][:-5] == "00000":
                                    tmpOk2[method] = "GOOD"
                                    OK2 = True
                                elif dist2[method]['DIST'] <= 10:
                                    tmpOk2[method] = "GOOD"
                                    OK2 = True

                        if OK2:
                            OK3 = False
                            startH = vecM[sM_idx - 1] if sM_idx != 0 else high
                            endH = samples_numM
                            vecH = range(startH, endH + high, high)
                            result_dict3 = {}
                            sample_start3 = 0
                            for sH_idx, samples_numH in enumerate(vecH, 0):
                                if OK3: break

                                result_df, result_dict3 = func.build_samples_from_file(p_list=p_list,
                                                                                       window_size=window_size,
                                                                                       sample_start=sample_start3,
                                                                                       sample_end=samples_numH,
                                                                                       result_dict=result_dict3)
                                sample_start3 = samples_numH
                                common_samples_df = func.prune_samples_extended(result_df, min_count=-1,
                                                                                quantile=quantile)

                                tmpOk3 = {}
                                dist3 = {}
                                retrieved_key3 = {}
                                candidate_key3 = {}
                                s1_match_indices3 = {}
                                for method in method_vec:
                                    if tmpOk2[method] == "BAD":
                                        tmpOk3[method] = tmpOk2[method]
                                        dist3[method] = dist2[method]
                                        candidate_key3[method] = candidate_key2[method]
                                        retrieved_key3[method] = retrieved_key2[method]
                                        s1_match_indices3[method] = s1_match_indices2[method]
                                        continue

                                    methodFun = methodFunDict[method]
                                    retrieved_key3[method] = methodFun(common_samples_df,
                                                                       stitch_shift_size,
                                                                       window_size)

                                    candidate_key3[method] = max(retrieved_key3[method], key=len)
                                    dist3[method], s1_match_indices3[method] = func.levenshtein_edit_dist(key,
                                                                                                 candidate_key3[
                                                                                                     method])

                                    tmpOk3[method] = "BAD"
                                    if dist3[method]['DIST'] < 25:
                                        if dist3[method]['DIST'] - dist3[method]['I'] <= 10 and \
                                                candidate_key3[method][:5] == "00000":
                                            tmpOk3[method] = "GOOD"
                                            OK3 = True
                                        elif dist3[method]['DIST'] - dist3[method]['I'] <= 10 and \
                                                candidate_key3[method][:-5] == "00000":
                                            tmpOk3[method] = "GOOD"
                                            OK3 = True
                                        elif dist3[method]['DIST'] <= 10:
                                            tmpOk3[method] = "GOOD"
                                            OK3 = True




                                if OK3:
                                    OK4 = False
                                    startFH = vecH[sH_idx - 1] if sH_idx != 0 else Fhigh
                                    endFH = samples_numH
                                    vecFH = range(startFH, endFH + Fhigh, Fhigh)
                                    result_dict4 = {}
                                    sample_start4 = 0
                                    for sFH_idx, samples_numFH in enumerate(vecFH, 0):
                                        if OK4: break

                                        result_df, result_dict4 = func.build_samples_from_file(p_list=p_list,
                                                                                               window_size=window_size,
                                                                                               sample_start=sample_start4,
                                                                                               sample_end=samples_numFH,
                                                                                               result_dict=result_dict4)
                                        sample_start4 = samples_numFH
                                        common_samples_df = func.prune_samples_extended(result_df, min_count=-1,
                                                                                        quantile=quantile)

                                        tmpOk4 = {}
                                        dist4 = {}
                                        retrieved_key4 = {}
                                        candidate_key4 = {}
                                        s1_match_indices4 = {}
                                        for method in method_vec:
                                            if tmpOk3[method] == "BAD":
                                                tmpOk4[method] = tmpOk3[method]
                                                dist4[method] = dist3[method]
                                                candidate_key4[method] = candidate_key3[method]
                                                retrieved_key4[method] = retrieved_key3[method]
                                                s1_match_indices4[method] = s1_match_indices3[method]
                                                continue

                                            methodFun = methodFunDict[method]
                                            retrieved_key4[method] = methodFun(common_samples_df,
                                                                               stitch_shift_size,
                                                                               window_size)

                                            candidate_key4[method] = max(retrieved_key4[method], key=len)
                                            dist4[method], s1_match_indices4[method] = func.levenshtein_edit_dist(key,
                                                                                                         candidate_key4[
                                                                                                             method])

                                            tmpOk4[method] = "BAD"
                                            if dist4[method]['DIST'] < 25:
                                                if dist4[method]['DIST'] - dist4[method]['I'] <= 10 and \
                                                        candidate_key4[method][:5] == "00000":
                                                    tmpOk4[method] = "GOOD"
                                                    OK4 = True
                                                elif dist4[method]['DIST'] - dist4[method]['I'] <= 10 and \
                                                        candidate_key4[method][:-5] == "00000":
                                                    tmpOk4[method] = "GOOD"
                                                    OK4 = True
                                                elif dist4[method]['DIST'] <= 10:
                                                    tmpOk4[method] = "GOOD"
                                                    OK4 = True



                                        if OK4:
                                            SAMPLE_NUM_PATH = "/samples_num{0}".format(samples_numFH)
                                            TryMkdir(
                                                DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH +
                                                WINDOWS_SIZE_PATH +
                                                QUANTILE_NUM_PATH +
                                                SAMPLE_LEN_PATH +
                                                SAMPLE_NUM_PATH)

                                            tableResult["cpuName_{0}".format(codeName)][
                                                "key_length{0}".format(key_length)][
                                                "window_size{0}".format(window_size)][
                                                "quantile{0}".format(quantile)][
                                                "probe_len{0}".format(probe_len)][
                                                "samples_num{0}".format(samples_numFH)] = {}

                                            tmpC = c
                                            for method in method_vec:
                                                if tmpOk4[method] == "BAD":

                                                    methodFun = methodFunDict[method]
                                                    retrieved_key4[method] = methodFun(common_samples_df,
                                                                                       stitch_shift_size,
                                                                                       window_size)

                                                    candidate_key4[method] = max(retrieved_key4[method], key=len)
                                                    dist4[method], s1_match_indices4[method] = func.levenshtein_edit_dist(
                                                        key,candidate_key4[method])

                                                    if dist4[method]['DIST'] < 25:
                                                        if dist4[method]['DIST'] - dist4[method]['I'] <= 10 and \
                                                                candidate_key4[method][:5] == "00000":
                                                            tmpOk4[method] = "GOOD"
                                                        elif dist4[method]['DIST'] - dist4[method]['I'] <= 10 and \
                                                                candidate_key4[method][:-5] == "00000":
                                                            tmpOk4[method] = "GOOD"
                                                        elif dist4[method]['DIST'] <= 10:
                                                            tmpOk4[method] = "GOOD"

                                                METHOD_PATH = "/{0}".format(method)
                                                TryMkdir(
                                                    DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH +
                                                    WINDOWS_SIZE_PATH +
                                                    QUANTILE_NUM_PATH +
                                                    SAMPLE_LEN_PATH +
                                                    SAMPLE_NUM_PATH +
                                                    METHOD_PATH)

                                                summryMy = open(
                                                    DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH +
                                                    WINDOWS_SIZE_PATH +
                                                    QUANTILE_NUM_PATH +
                                                    SAMPLE_LEN_PATH +
                                                    SAMPLE_NUM_PATH +
                                                    METHOD_PATH + "/summryMy.txt", "w")

                                                if PRINT_RETRIVED_KESYS:
                                                    retrievedKeysFile = open(
                                                        DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH +
                                                        KEY_LENGTH_PATH +
                                                        WINDOWS_SIZE_PATH +
                                                        QUANTILE_NUM_PATH +
                                                        SAMPLE_LEN_PATH +
                                                        SAMPLE_NUM_PATH +
                                                        METHOD_PATH + "/retrievedKeys.txt", "w")

                                                    for cankey in retrieved_key4[method]:
                                                        if len(cankey) > SIZE_OF_RETRIVED_KESYS_TO_PRINT * len(key):
                                                            retrievedKeysFile.write(cankey)
                                                            retrievedKeysFile.write("\n")
                                                    retrievedKeysFile.close()

                                                PrintToSummryFile(summryMy, key, key_length, candidate_key4[method],
                                                                  samples_numFH,
                                                                  result_df,
                                                                  quantile, common_samples_df, stitch_shift_size,
                                                                  window_size, dist4[method], s1_match_indices4[method])

                                                string = "\nDIST-INSERTION = " + str(
                                                    dist4[method]['DIST'] - dist4[method]['I'])
                                                summryMy.write(string)
                                                summryMy.close()

                                                dist4[method]['DIST - INSERTIONS'] = \
                                                    dist4[method]['DIST'] - dist4[method]['I']

                                                # ---------------------------------------------
                                                worksheetQ.write(0, tmpC, int(dist4[method]['DIST']))
                                                worksheetQ.write(1, tmpC, str(dist4[method]))
                                                worksheetQ.write(2, tmpC, tmpOk4[method])
                                                worksheetQ.write(3, tmpC, int(samples_numFH))

                                                #---------------------------------------------
                                                worksheet.write(r, tmpC, int(dist4[method]['DIST']))
                                                worksheet.write(r + 1, tmpC, str(dist4[method]))
                                                worksheet.write(r + 2, tmpC, tmpOk4[method])
                                                worksheet.write(r + 3, tmpC, int(samples_numFH))
                                                tmpC += 1

                                                dist4[method]["Ok"] = tmpOk4[method]

                                                tableResult["cpuName_{0}".format(codeName)][
                                                    "key_length{0}".format(key_length)][
                                                    "window_size{0}".format(window_size)][
                                                    "quantile{0}".format(quantile)][
                                                    "probe_len{0}".format(probe_len)][
                                                    "samples_num{0}".format(samples_numFH)]["{0}".format(method)] = dist4[method]



                                                tableFileP = open(DIR_RESULT_PATH +
                                                                  DIR_PATH_REALCHANNEL +
                                                                  CODE_NAME_PATH +
                                                                  KEY_LENGTH_PATH +
                                                                  WINDOWS_SIZE_PATH +
                                                                  QUANTILE_NUM_PATH +
                                                                  "/real{0}_W{1}_Q{2}_probe{3}.json".format(key_length, window_size, quantile, probe_len),
                                                                  "w")
                                                tableFileP.write(
                                                    str(tableResult["cpuName_{0}".format(codeName)][
                                                    "key_length{0}".format(key_length)][
                                                    "window_size{0}".format(window_size)][
                                                    "quantile{0}".format(quantile)][
                                                    "probe_len{0}".format(probe_len)])
                                                )
                                                tableFileP.close()



                                                tableFileQ = open(DIR_RESULT_PATH +
                                                                  DIR_PATH_REALCHANNEL +
                                                                  CODE_NAME_PATH +
                                                                  KEY_LENGTH_PATH +
                                                                  WINDOWS_SIZE_PATH +
                                                                  "/real{0}_W{1}_Q{2}.json".format(key_length,window_size,quantile),
                                                                  "w")
                                                tableFileQ.write(str(tableResult["cpuName_{0}".format(codeName)][
                                                    "key_length{0}".format(key_length)][
                                                    "window_size{0}".format(window_size)][
                                                    "quantile{0}".format(quantile)]))
                                                tableFileQ.close()



                                                tableFile = open(DIR_RESULT_PATH +
                                                                 DIR_PATH_REALCHANNEL +
                                                                 "/real{0}.json".format(key_length),
                                                                 "w")
                                                tableFile.write(str(tableResult))
                                                tableFile.close()

        workbookQ.close()
    workbook.close()
