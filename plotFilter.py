#! /usr/bin/python
import numpy as np
import pandas as pd
import key_stitching_functinos as func
import os
import matplotlib.pyplot
import plotly.graph_objs as go
import plotly.offline as ply
import pickle


def Probe(probe_len, codeName):
    paths = {
        "SandyBrige":
            {
                180: [],
                230: ["./samples/SandyBrige/new_2048_probe230/good_decoded_samples.txt"],
                300: [],
            },
        "Haswell":
            {
                180: ["./samples/Haswell/key1/probe180/good_decoded_samples.txt"],
                200: ["./samples/Haswell/key1/probe230/good_decoded_samples.txt"],
		        230: ["./samples/Haswell/key1/probe230_stress/good_decoded_samples.txt"],
                300: ["./samples/Haswell/key1/probe300/good_decoded_samples.txt"],
            },
        "CoffeeLake":
            {
                180: [],
                230: ["./samples/CoffeeLake/stress/good_decoded_samples_idle256.txt"],
                300: [],
            },
        "SkyLake":
            {
                180: [],
                230: ["./samples/Skylake/key1/good_decoded_samples_v1.txt"],
                300: [],
            },
    }
    return paths[codeName][probe_len]




p_list = Probe(200, "Haswell")
result_dict={}
# result_df, result_dict = func.build_samples_from_file(p_list=p_list,window_size=30, sample_start=0, sample_end=100000,result_dict=result_dict)
key = func.init_key(1024, -1)

result_df, result_dict = func.build_samples_continues(key=key,
                                                      sample_begin=0,
                                                      sample_end=3000,
                                                      sample_len=40,
                                                      window_size=30,
                                                      flip_probability=0.01,
                                                      delete_probability=0.01,
                                                      insert_probability=0.01,
                                                      result_dict=result_dict)

result_df=result_df.sort_values('count', ascending=False)
'''
trace = go.Bar(
    #x=result_df['sample'],
    y=result_df['count'],
    name="Levenshtein Dist graph",
)
# Create traces - data collections
# Create information / layout dictionary
layout = dict(
    title="filter",


    xaxis={'title': 'samples'},
    yaxis={'title': 'count',
           'range': [0, 2]}
)
# Pack the data
data = [trace]
# Create a figure
fig = dict(data=data, layout=layout)
# Plot
ply.plot(fig, filename='./filterGraph.html')
# ply.plot(data, filename='./filterGraph.html')

'''
# import plotly.express as px
# fig = px.bar(result_df,  y='count')
# fig.show()

result_df.plot.bar(y='count', rot=0)
matplotlib.pyplot.show()