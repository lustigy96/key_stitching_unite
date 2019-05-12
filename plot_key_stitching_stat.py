#! /usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import math 

def side_by_side_bars(x,y_vec,colors,title,ind,width,x_label, y_label):
	x=np.array(x)
	fig = plt.figure(ind)
	plt.title(title)
	plt.xlabel(x_label)
	plt.ylabel(y_label)
	ax = fig.add_subplot(111)
	i=-(len(y_vec)/2)*width
	width_f=0.27 
	rects=[]
	
	for y,c in zip(y_vec,colors):
		rect= ax.bar(ind,width_f,color=c)
		rects.append(rect)

		ax.bar(x-i, y,width=width,color=c,align='center')
		for x_tag, tolabel in zip(x,y):
			ax.text(x_tag-i + .25, tolabel + 3,str(tolabel), color='k',  ha='center')
		i+=width
		
	ax.legend( (rects), ('dist', 'I', 'D','F','|L|') )
	


if __name__ == "__main__":

	x_label = raw_input('Enter x label (for example: samples number) default=0: ') 
	graph_name = raw_input('Enter graph label (for example: window size) default=0: ') 
	if x_label=='0': x_label="sampeles number"
	if graph_name=='0': graph_name="window size"
		
	print "bla"
	y_label = "distance"
	
	f_data=open("./results/NoDict/simulation/CASE5/dataForGraph_Key=None_Graphs=KEYLENGTH_x=megicNumVec_windowSize=30_quantile=0.6.txt","r")
	#f_data=open("./results/data.txt","r")
	lines=f_data.readlines()
	window_size= map(int, lines[0].split(" "))
	sump_num=map(int, lines[1].split(" "))
	

	if len(sump_num)>1:
		diff = min([j-i for i, j in zip(sump_num[:-1], sump_num[1:])])
		width = math.ceil((diff/4)/2);
	else: 
		width=12000
	
	colors=['k','b','r','g','purple']

	i=1
	ind=0
	for w in window_size:
		ind+=1
		dist,insertions,deletions,flips, length=[],[],[],[],[]
		for n in sump_num:
			i+=1
			line=np.array(lines[i].split(" ")).astype(int)
			dist.append(line[0])
			deletions.append(line[1])
			insertions.append(line[2])			
			flips.append(line[3])
			length.append(line[4])
		y_vec=[dist,insertions, deletions, flips, length]
		title= y_label+" results for "+graph_name+" "+str(w)
		
		side_by_side_bars(sump_num,y_vec,colors,title,ind,width,x_label,y_label)

	f_data.close()
	plt.show()
