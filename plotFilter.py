#! /usr/bin/python
import numpy as np
import pandas as pd
import key_stitching_functinos as func
import os
import matplotlib.pyplot
import plotly.graph_objs as go
import plotly.offline as ply
import pickle


result_dict={}
# result_df, result_dict = func.build_samples_from_file(p_list=p_list,window_size=30, sample_start=0, sample_end=100000,result_dict=result_dict)
key = func.init_key(512, -1)

result_df, result_dict = func.build_samples_continues(key=key,
                                                      sample_begin=0,
                                                      sample_end=500000,
                                                      sample_len=45,
                                                      window_size=30,
                                                      flip_probability=0.05,
                                                      delete_probability=0.05,
                                                      insert_probability=0.05,
                                                      result_dict=result_dict)

result_df=result_df.sort_values('count', ascending=False)
result_df= result_df[result_df['count']>1]
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
    hover_data=['lifeExp', 'gdpPercap'],
    color='lifeExp',
    xaxis={'title': 'samples'},
    yaxis={'title': 'count',
           'range': [0, 2]}
)
# Pack the data
data = [trace]
# Create a figure
# fig = dict(data=data, layout=layout)
# Plot

import plotly.express as px
fig = px.bar(result_df,  y='count', color='count')
ply.plot(fig, filename='./filterGraph.html')
# fig.show()
'''

result_df.plot.bar(y='count', rot=0)
matplotlib.pyplot.show()