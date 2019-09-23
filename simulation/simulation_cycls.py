#! /usr/bin/python




import xlsxwriter

import key_stitching_functinos as func
from simulation import help_staf as help
from simulation.help_staf import TryMkdir





# if __name__ == "__main__":


SIMULATION = True

DIR_RESULT_PATH = "./results"
DIR_PATH_SIMULATION = "/simulation"

PRINT_RETRIVED_KESYS = True
SIZE_OF_RETRIVED_KESYS_TO_PRINT = 0.995

p = TryMkdir(DIR_RESULT_PATH)
p = TryMkdir(p + DIR_PATH_SIMULATION)
fragemnt_len_vec = [30]
window_size_vec = [25]  # each has its own graph
stitch_shift_size = 1
quantile_vec = [0.9, 0.6]  # each has
method_vec = ["cycle"]  # ["notOpposite","Opposite"]
error_vec = [3]

OK1=False
i = 0
key_length=2048
key = func.init_key(key_length, -1)


tableResult = {}
KEY_LENGTH_PATH = "/key_length{0}".format(key_length)
p = TryMkdir(p + KEY_LENGTH_PATH)









for quantile in quantile_vec:

    workbookQ = xlsxwriter.Workbook(p + '/simulation_table{0}_q{1}.xlsx'.format(key_length, quantile))
    worksheetQ = workbookQ.add_worksheet()

    tableResult\
        ["key_length{0}".format(key_length)] = {}

    QUANTILE_NUM_PATH = "/quantile{0}".format(quantile)
    TryMkdir(p + QUANTILE_NUM_PATH)

    tableResult \
        ["key_length{0}".format(key_length)] \
        ["quantile{0}".format(quantile)] = {}

    col = -2

    for fragemnt_len in fragemnt_len_vec:
        col += 2

        SAMPLE_LEN_PATH = "/fragemnt_len{0}".format(fragemnt_len)
        TryMkdir(p + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH)

        tableResult \
            ["key_length{0}".format(key_length)] \
            ["quantile{0}".format(quantile)] \
            ["fragemnt_len{0}".format(fragemnt_len)] = {}


        for error in error_vec:

            if OK1: break

            error_dict = help.Error(error)
            samples_num_vec = error_dict["samples_num_vec"]

            ERROR_PATH = "/error{0}".format(error)

            TryMkdir(p + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH + ERROR_PATH)
            tableResult \
                ["key_length{0}".format(key_length)] \
                ["quantile{0}".format(quantile)] \
                ["fragemnt_len{0}".format(fragemnt_len)] \
                ["error{0}".format(error)]= {}


            row = -2
            for window_size in window_size_vec:
                if OK1: break
                row += 2
                WINDOWS_SIZE_PATH = "/window_size{0}".format(window_size)
                TryMkdir(p + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH + ERROR_PATH + WINDOWS_SIZE_PATH)

                tableResult \
                    ["key_length{0}".format(key_length)] \
                    ["quantile{0}".format(quantile)] \
                    ["fragemnt_len{0}".format(fragemnt_len)] \
                    ["error{0}".format(error)] \
                    ["window_size{0}".format(window_size)] = {}

                start_samp = 0
                result_dict = {}


                col=0
                for samples_num in samples_num_vec:
                    if OK1: break
                    SAMPLE_NUM_PATH = "/samples_num{0}".format(samples_num)
                    TryMkdir(p + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH + ERROR_PATH + WINDOWS_SIZE_PATH + SAMPLE_NUM_PATH)
                    tableResult \
                        ["key_length{0}".format(key_length)] \
                        ["quantile{0}".format(quantile)] \
                        ["fragemnt_len{0}".format(fragemnt_len)] \
                        ["error{0}".format(error)] \
                        ["window_size{0}".format(window_size)] \
                        ["samples_num{0}".format(samples_num)] = {}

                    result_df, result_dict = func.build_samples_continues(key=key,
                                                                          sample_begin=start_samp,
                                                                          sample_end=samples_num,
                                                                          sample_len=fragemnt_len,
                                                                          window_size=window_size,
                                                                          flip_probability=error_dict["flip"],
                                                                          delete_probability=error_dict["del"],
                                                                          insert_probability=error_dict["insert"],
                                                                          result_dict=result_dict)
                    start_samp = samples_num
                    common_samples_df = func.prune_samples_extended(result_df, -1, quantile)


                    tmpOk = {}
                    dist = {}
                    retrieved_key = {}
                    candidate_key = {}
                    s1_match_indices = {}
                    tmpC = col

                    for method in method_vec:
                        METHOD_PATH = "/{0}".format(method)
                        TryMkdir(p + QUANTILE_NUM_PATH + SAMPLE_LEN_PATH + ERROR_PATH + WINDOWS_SIZE_PATH +
                                 SAMPLE_NUM_PATH + METHOD_PATH)

                        methodFun = help.methodFunDict[method]

                        tree_pointers, edge_left_pointers, common_samples_array = func.build_shift_pointers_tree(common_samples_df, stitch_shift_size, window_size)
                        retrieved_key[method] = func.stitch_with_cycles(tree_pointers, edge_left_pointers, common_samples_array)

                        candidate_key[method] = max(retrieved_key[method], key=len)
                        dist[method], s1_match_indices[method] = func.levenshtein_edit_dist(key, candidate_key[method])

                        dist[method]['number_of_window_size_samples'] = len(result_df)
                        dist[method]['DIST - INSERTIONS'] = dist[method]['DIST'] - dist[method]['I']

                        dist[method]["Ok"] = "BAD"
                        if dist[method]['DIST'] <= 10:
                            dist[method]["Ok"] = "GOOD"
                            OK1=True

                        tableResult \
                            ["key_length{0}".format(key_length)] \
                            ["quantile{0}".format(quantile)] \
                            ["fragemnt_len{0}".format(fragemnt_len)] \
                            ["error{0}".format(error)] \
                            ["window_size{0}".format(window_size)] \
                            ["samples_num{0}".format(samples_num)] \
                            ["{0}".format(method)] = dist[method]

                        summryMy = open(p +
                                        QUANTILE_NUM_PATH +
                                        SAMPLE_LEN_PATH +
                                        ERROR_PATH +
                                        WINDOWS_SIZE_PATH +
                                        SAMPLE_NUM_PATH +
                                        METHOD_PATH + "/summryMy.txt", "w")

                        if PRINT_RETRIVED_KESYS:
                            retrievedKeysFile = open(p +
                                                     QUANTILE_NUM_PATH +
                                                     SAMPLE_LEN_PATH +
                                                     ERROR_PATH +
                                                     WINDOWS_SIZE_PATH +
                                                     SAMPLE_NUM_PATH +
                                                     METHOD_PATH + "/retrievedKeys.txt", "w")

                            for cankey in retrieved_key[method]:
                                if len(cankey) > SIZE_OF_RETRIVED_KESYS_TO_PRINT * len(key):
                                    retrievedKeysFile.write(cankey)
                                    retrievedKeysFile.write("\n")
                            retrievedKeysFile.close()

                        help.PrintToSummryFile(summryMy, key, key_length, candidate_key[method], samples_num, result_df,
                                          quantile, common_samples_df, stitch_shift_size, window_size, dist[method],
                                          s1_match_indices[method])





                        # ---------------------------------------------------
                        worksheetQ.write(0, tmpC, int(dist[method]['DIST']))
                        worksheetQ.write(1, tmpC, str(dist[method]))
                        worksheetQ.write(2, tmpC, dist[method]["Ok"])
                        worksheetQ.write(3, tmpC, int(samples_num))
                        worksheetQ.write(4, tmpC, len(result_df))
                        tmpC += 1

                        # -----------------------------------------------------
                        tableFile = open(p +"/simulation{0}.json".format(key_length), "w")
                        tableFile.write(str(tableResult))
                        tableFile.close()

    workbookQ.close()

















