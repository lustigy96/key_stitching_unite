import plotly
import plotly.graph_objs as go
import plotly.offline as ply
from plotly import tools
import os
import numpy as np

if __name__ == "__main__":


    try:
        os.mkdir("./results/")
    except:
        pass


    # x_label = raw_input('Enter x label (for example: samples number) default=0: ')
    x_label = "megicNumVec"
    # graph_name = raw_input('Enter graph label (for example: window size) default=0: ')
    graph_name = "KEYLENGTH"
    # path_to_file = raw_input('Enter path to the data file (for example: ./results/data.txt) default=0: ')
    path_to_file = "0"
    if path_to_file == '0':
        path_to_file = "./results/simulation/CASE5/dataForGraph_Key=None_Graphs=KEYLENGTH_x=megicNumVec_windowSize=30_quantile=0.6.txt"

    f_data = open(path_to_file,"r")
    lines = f_data.readlines()
    graphs = map(int, lines[0].split(" "))

    x = map(int, lines[1].split(" "))


    if graph_name == '0':
        graph_name = "WINDOES" # QUANTILE
    if x_label == '0':
        x_label= "samplesNumVec"

    # dict = {"DIST":None, "I":None, "D":None,"F":None, "|L|":None}
    # fig = tools.make_subplots(rows=len(graphs), cols=1)
    # fig = tools.make_subplots(rows=1, cols=1)
    # fig['layout'].update(title='range25to30')
    # data = []
    # subplot_titles = []
    #
    i = 1
    for graph in graphs:
        name = '{0} = {1}'.format(graph_name,graph)
        trace=[]
        dist, insertions, deletions, flips, length = [], [], [], [], []
        for element in x:
            i += 1

            line = np.array(lines[i].split(" ")).astype(int)
            dist.append(line[0])
            deletions.append(line[1])
            insertions.append(line[2])
            flips.append(line[3])
            length.append(line[4])

        trace_dist = go.Bar(
            x=x,
            y=dist,
            name="dist"
        )

        trace_deletions = go.Bar(
            x=x,
            y=deletions,
            name="deletions"
        )

        trace_insertions = go.Bar(
            x=x,
            y=insertions,
            name="insertions"
        )

        trace_flips = go.Bar(
            x=x,
            y=flips,
            name="flips"
        )

        trace_length = go.Bar(
            x=x,
            y=length,
            name="length"
        )

        layout = go.Layout(
            title=name
        )

        data = [trace_dist,trace_deletions,trace_insertions,trace_flips,length ]
        fig = go.Figure(data=data,layout=layout)
        # fig.append_trace(trace, i, 1)
        # i += 1

        # Create a figure
        ply.plot(fig, filename='./results/{0}.html'.format(name))
