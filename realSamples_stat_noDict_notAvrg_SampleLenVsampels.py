#! /usr/bin/python
#
import numpy as np
import pandas as pd
import key_stitching_functinos as func
import os
import xlsxwriter

def Probe(probe_len, codeName):
    paths = {
        "Haswell":
            {
                180: [],
                230: ["./samples/Haswell/probe230/good_decoded_samples.txt"],
                300: [],
            },
        "CoffeeLake":
            {
                200: ["./samples/CoffeeLake/200/good_decoded_samples.txt"],
                230: ["./samples/CoffeeLake/230/good_decoded_samples.txt"],
                300: ["./samples/CoffeeLake/300/good_decoded_samples.txt"],
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


def opposite(common_samples_df, stitch_shift_size, window_size):
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


if __name__ == "__main__":

    DIR_RESULT_PATH = "./results"
    DIR_PATH_REALCHANNEL = "/realChannel"
    PRINT_RETRIVED_KESYS = True
    SIZE_OF_RETRIVED_KESYS_TO_PRINT = 0.995

    try:
        os.mkdir(DIR_RESULT_PATH)
    except:
        pass

    try:
        os.mkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL)
    except:
        pass

    print "\n\n~~Start SFS Algorithem...~~\n\n"

    hex_key_512 = "023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd"
    hex_key_1024 = "023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f"
    hex_key_2048 = "023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e70f808182838485868788898a8b8c8d8e8909192939495969798999a9b9c9d9e91a0a1a2a3a4a5a6a7a8a9aaabacadaea1b0b1b2b3b4b5b6b7b8b9babbbcbdbeb1c0c1c2c3c4c5c6c7c8c9cacbcccdcec1"
    hex_key_4096 = "023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e70f808182838485868788898a8b8c8d8e8909192939495969798999a9b9c9d9e91a0a1a2a3a4a5a6a7a8a9aaabacadaea1b0b1b2b3b4b5b6b7b8b9babbbcbdbeb1c0c1c2c3c4c5c6c7c8c9cacbcccdcec1d0d1d2d3d4d5d6d7d8d9dadbdcddded1e0e1e2e3e4e5e6e7e8e9eaebecedeee1f0f1f2f3f4f5f6f7f8f91a1b1c1d1e1f123456789abcdef1dcba9876543215211815222936435057647178859299106113120127134141148155162169176183190197203210217224231239246253260267274281289296303310317324331301123581321345589144233377610987159725844181676510946177112865746368750251213931964183178115142298320401346269217830935245785702123456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd"

    key512 = ''.join(func.hex2bin_map[i] for i in hex_key_512)
    key1024 = ''.join(func.hex2bin_map[i] for i in hex_key_1024)
    key2048 = ''.join(func.hex2bin_map[i] for i in hex_key_2048)
    key4096 = ''.join(func.hex2bin_map[i] for i in hex_key_4096)

    key_length_vec = [len(key2048)]  # [len(key512), len(key1024), len(key2048),len(key4096)]
    key_vec = [key2048]  # [key512, key1024, key2048, key4096]
    probe_len_vec = [200, 300,400,550,700]  # [180, 230, 300]
    window_size_vec = [30]
    samples_num_vec = [50000, 100000,150000,200000,250000,300000,350000,  400000,450000,500000]
    quantile_vec = [0.6,0.9]  # each has
    method_vec = ["notOpposite", "Opposite"]
    cpuName = ["CoffeeLake"]#["Haswell"]  # ["SandyBrige", "Haswell", "CoffeeLake","SkyLake"]
    stitch_shift_size = 1

    tableResult = {}

    i = 0
    for codeName in cpuName:
        CODE_NAME_PATH = "/cpuName_{0}".format(codeName)
        try:
            os.mkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH)
        except:
            pass
        tableResult["cpuName_{0}".format(codeName)] = {}

        for idxK, key_length in enumerate(key_length_vec):
            key = key_vec[idxK]
            KEY_LENGTH_PATH = "/key_length{0}".format(key_length)
            try:
                os.mkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH)
            except:
                pass
            tableResult["cpuName_{0}".format(codeName)]["key_length{0}".format(key_length)] = {}

            workbook = xlsxwriter.Workbook(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH +
                                           '/simulation_table{0}.xlsx'
                                           .format(key_length_vec[0]))

            worksheet = workbook.add_worksheet()

            for window_size in window_size_vec:
                WINDOWS_SIZE_PATH = "/window_size{0}".format(window_size)
                try:
                    os.mkdir(
                        DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH +
                        WINDOWS_SIZE_PATH)
                except:
                    pass
                    tableResult["cpuName_{0}".format(codeName)][
                        "key_length{0}".format(key_length)][
                        "window_size{0}".format(window_size)] = {}


                r=-3
                for quantile in quantile_vec:
                    r+=3
                    QUANTILE_NUM_PATH = "/quantile{0}".format(quantile)
                    try:
                        os.mkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH +
                                 WINDOWS_SIZE_PATH +
                                 QUANTILE_NUM_PATH)
                    except:
                        pass
                    tableResult["cpuName_{0}".format(codeName)][
                        "key_length{0}".format(key_length)][
                        "window_size{0}".format(window_size)]["quantile{0}".format(quantile)] = {}

                    c=-2

                    for probe_len in probe_len_vec:

                        c+=2
                        p_list = Probe(probe_len=probe_len, codeName=codeName)

                        SAMPLE_LEN_PATH = "/probe_len{0}".format(probe_len)

                        try:
                            os.mkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH +
                                     WINDOWS_SIZE_PATH +
                                     QUANTILE_NUM_PATH +
                                     SAMPLE_LEN_PATH)
                        except:
                            pass

                        tableResult["cpuName_{0}".format(codeName)][
                            "key_length{0}".format(key_length)][
                            "window_size{0}".format(window_size)][
                            "quantile{0}".format(quantile)][
                            "probe_len{0}".format(probe_len)] = {}

                        ok = False
                        for samples_num in samples_num_vec:
                            if ok: break


                            SAMPLE_NUM_PATH = "/samples_num{0}".format(samples_num)
                            try:
                                os.mkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH +
                                         WINDOWS_SIZE_PATH +
                                         QUANTILE_NUM_PATH +
                                         SAMPLE_LEN_PATH +
                                         SAMPLE_NUM_PATH)
                            except:
                                pass
                            tableResult["cpuName_{0}".format(codeName)][
                                "key_length{0}".format(key_length)][
                                "window_size{0}".format(window_size)][
                                "quantile{0}".format(quantile)][
                                "probe_len{0}".format(probe_len)][
                                "samples_num{0}".format(samples_num)] = {}


                            start_samp = 0
                            result_dict = {}



                            result_df, result_dict = func.build_samples_from_file(p_list=p_list,
                                                                                              window_size=window_size,
                                                                                              sample_start=start_samp,
                                                                                              sample_end=samples_num,
                                                                                              result_dict=result_dict)
                            start_samp = samples_num



                            common_samples_df = func.prune_samples_extended(result_df, min_count=-1, quantile=quantile)
                            tmpC = c
                            for method in method_vec:
                                METHOD_PATH = "/{0}".format(method)
                                try:
                                    os.mkdir(DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + CODE_NAME_PATH + KEY_LENGTH_PATH +
                                         WINDOWS_SIZE_PATH +
                                         QUANTILE_NUM_PATH +
                                         SAMPLE_LEN_PATH +
                                         SAMPLE_NUM_PATH +
                                             METHOD_PATH)
                                except:
                                    pass
                                tableResult["cpuName_{0}".format(codeName)][
                                    "key_length{0}".format(key_length)][
                                    "window_size{0}".format(window_size)][
                                    "quantile{0}".format(quantile)][
                                    "probe_len{0}".format(probe_len)][
                                    "samples_num{0}".format(samples_num)]["{0}".format(method)] = {}

                                if method == "notOpposite":
                                    retrieved_key = notOpposite(common_samples_df, stitch_shift_size, window_size)
                                elif method == "Opposite":
                                    retrieved_key = opposite(common_samples_df, stitch_shift_size, window_size)

                                candidate_key = max(retrieved_key, key=len)

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

                                    for cankey in retrieved_key:
                                        if len(cankey) > SIZE_OF_RETRIVED_KESYS_TO_PRINT * len(key):
                                            retrievedKeysFile.write(cankey)
                                            retrievedKeysFile.write("\n")

                                    retrievedKeysFile.close()

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
                                         "\nF = " + str(dist['F'])

                                tmpOk = False
                                dist['DIST - INSERTIONS'] = -1
                                if dist['DIST'] <25:
                                    if dist['DIST']-dist['I']>10 and candidate_key[:5]=="00000":
                                        string = string + "\nDIST-INSERTION = " + str(dist['DIST']-dist['I'])
                                        ok = True
                                        tmpOk = True
                                        dist['DIST - INSERTIONS'] = dist['DIST'] - dist['I']

                                    elif dist['DIST']-dist['I']<=10:
                                        ok = True
                                        tmpOk = True

                                worksheet.write(r, tmpC, int(dist['DIST']))
                                # worksheet.write(r+1, c, int(dist['DIST']-dist['I']))
                                worksheet.write(r+1, tmpC, str(dist))
                                worksheet.write(r+2, tmpC, str("GOOD") if tmpOk else str ("BAD"))


                                summryMy.write(string)
                                summryMy.close()

                                tableResult["cpuName_{0}".format(codeName)][
                                    "key_length{0}".format(key_length)][
                                    "window_size{0}".format(window_size)][
                                    "quantile{0}".format(quantile)][
                                    "probe_len{0}".format(probe_len)][
                                    "samples_num{0}".format(samples_num)]["{0}".format(method)] = dist



                                tableFile = open(
                                    DIR_RESULT_PATH + DIR_PATH_REALCHANNEL + "/real_table{0}.txt".format(
                                        key_length), "w")
                                tableFile.write(str(tableResult))
                                tableFile.close()
                                tmpC +=1

                workbook.close()



