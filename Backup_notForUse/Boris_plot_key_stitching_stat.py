import plotly
import plotly.graph_objs as go
import plotly.offline as ply
from plotly import tools
import os
import numpy as np

if __name__ == "__main__":
    SUBPLOTS = True

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
        path_to_file = "./results/NoDict/simulation/CASE5/dataForGraph_Key=None_Graphs=KEYLENGTH_x=megicNumVec_windowSize=30_quantile=0.6.txt"

    f_data = open(path_to_file,"r")
    lines = f_data.readlines()
    graphs = map(int, lines[0].split(" "))

    x = map(int, lines[1].split(" "))


    if graph_name == '0':
        graph_name = "WINDOES" # QUANTILE
    if x_label == '0':
        x_label= "samplesNumVec"


    if SUBPLOTS:
        fig = tools.make_subplots(rows=len(graphs), cols=1, subplot_titles= tuple(graphs))
        fig['layout'].update(title=str(graph_name))


    j= i = 1
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
            text=dist,
            textposition='auto',
            name="dist{0}".format(graph)
        )

        trace_deletions = go.Bar(
            x=x,
            y=deletions,
            text=deletions,
            textposition='auto',
            name="deletions{0}".format(graph)
        )

        trace_insertions = go.Bar(
            x=x,
            y=insertions,
            text=insertions,
            textposition='auto',
            name="insertions{0}".format(graph)
        )

        trace_flips = go.Bar(
            x=x,
            y=flips,
            text=flips,
            textposition='auto',
            name="flips{0}".format(graph)
        )

        trace_length = go.Bar(
            x=x,
            y=length,
            text=length,
            textposition='auto',
            name="length{0}".format(graph)
        )



        data = [trace_dist,trace_deletions,trace_insertions,trace_flips,trace_length ]

        if SUBPLOTS:
            fig.append_trace(trace_dist, j, 1)
            fig.append_trace(trace_deletions, j, 1)
            fig.append_trace(trace_insertions, j, 1)
            fig.append_trace(trace_flips, j, 1)
            fig.append_trace(trace_length, j, 1)
            j += 1
        else:
            layout = go.Layout(title=str(name))
            fig = go.Figure(data=data, layout=layout)
            ply.plot(fig, filename='./results/{0}.html'.format(name))

        # Create a figure
    if SUBPLOTS:
        ply.plot(fig, filename='./results/{0}.html'.format(graph_name))
