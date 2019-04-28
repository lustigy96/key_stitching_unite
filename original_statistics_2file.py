import key_stitching_functinos as func
import numpy as np


hex2bin_map = {
   "0":"0000",
   "1":"0001",
   "2":"0010",
   "3":"0011",
   "4":"0100",
   "5":"0101",
   "6":"0110",
   "7":"0111",
   "8":"1000",
   "9":"1001",
   "a":"1010",
   "b":"1011",
   "c":"1100",
   "d":"1101",
   "e":"1110",
   "f":"1111"
}
#hex_key_2048="023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e70f808182838485868788898a8b8c8d8e8909192939495969798999a9b9c9d9e91a0a1a2a3a4a5a6a7a8a9aaabacadaea1b0b1b2b3b4b5b6b7b8b9babbbcbdbeb1c0c1c2c3c4c5c6c7c8c9cacbcccdcec1"
hex_key_500="023456789abcdef1dcba987654321112233445566778899aabbccddeef1eeddccbbaa99887766554433221100111222333444555666777888999aaabbbcccddd"
key=''.join(hex2bin_map[i] for i in hex_key_500)
#path="C:/YAEL/BGU/data_for_proj/key_stich/good_decoded_samples.txt"
path="/home/ubu/Yael/results/key500_probe300_good_decoded_samples_486K.txt"
key_length= 2048
stitch_shift_size = 2
window_size=30
window_size_vec = [20, 30]
samples_num_vec = [100000, 200000, 300000]
start_samp = 0
result_dict = {};
F_CSV_SAMPLES = "./results/key500_probe300_good_decoded_samples_486K.csv"

f_key_res = open("/home/ubu/Yael/results/key_res.txt", "w")
f_data = open("/home/ubu/Yael/results/data.txt", "w")

f_key_res.write("-------key------\n" + key + '\n')
f_data.write(' '.join(window_size_vec))
f_data.write(' '.join(samples_num_vec))

for window_size in window_size_vec:
    for samples_num in samples_num_vec:
        result_df, result_dict = func.build_samples_from_file(path, window_size, start_samp, samples_num, result_dict)
        common_samples_df = func.prune_samples_yael_extended(result_df, min_count=-1)
        shift_pointers = func.build_shift_pointers(np.array(common_samples_df['sample']), stitch_shift_size)
        retrieved_key = func.stitch(np.array(common_samples_df['sample']), shift_pointers)
        candidate_key = max(retrieved_key, key=len)
        f_key_res.write(
            '\n\nsamples: ' + str(samples_num) + ", window: " + str(window_size) + "\n" + candidate_key + '\n')
        f_key_res.write("len: " + str(len(candidate_key)))
        f_key_res.write("find: " + str(key.find(candidate_key)))
        dist = func.levenshtein_edit_dist(candidate_key, key, False)[0]
        f_data.write(str(dist['DIST']) + " " + str(dist['I']) + " " + str(dist['D']) + " " + str(dist['F']) + " " + str(
            len(key) - len(candidate_key)) + "\n")
        f_candidates = open("/home/ubu/Yael/results/candidates_" + str(window_size) + "_" + str(samples_num) + ".txt",
                            "w")
        for cand in retrieved_key:
            if len(cand) > 300:
                f_candidates.write(cand)
                f_candidates.write("\n")
        f_candidates.close()

f_data.close()
f_key_res.close()