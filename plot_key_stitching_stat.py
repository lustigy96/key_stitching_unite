import matplotlib.pyplot as plt
import numpy as np

def side_by_side_bars(x,y_vec,colors,title,ind):
	x=np.array(x)
	fig = plt.figure(ind)
	ax = fig.add_subplot(111)
	i=-(len(y_vec)/2)*5000
	width_f=0.27 
	rects=[]
	
	
	for y,c in zip(y_vec,colors):
		rect= ax.bar(ind,width_f,color=c)
		rects.append(rect)
		ax.bar(x-i, y,width=5000,color=c,align='center')
		i+=5000
	ax.legend( (rects), ('dist', 'I', 'D','F','|L|') )




f_data=open("/home/ubu/Yael/results/dist_res.txt","r")
lines=f_data.readlines()
window_size= map(int, lines[0].split(" "))  
sump_num=map(int, lines[1].split(" ")) 

colors=['b','r','g','y','m']

i=1
ind=0
for w in window_size:
	ind+=1
	dist,insertions,deletions,flips, length=[],[],[],[],[]
	for n in sump_num:
		i+=1
		line=np.array(lines[i].split(" ")).astype(int)
		dist.append(line[0])
		insertions.append(line[1])
		deletions.append(line[2])
		flips.append(line[3])
		length.append(line[4])
	y_vec=[dist,insertions, deletions, flips, length]
	title="distance results for window size "+str(w)
	side_by_side_bars(sump_num,y_vec,colors,title,ind)

f_data.close()
plt.show()
