# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 23:33:08 2018

@author: Samqua
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime
import random
import os

from geodesic import *

iterations=0
plotAll=True
numbins=80
filename="eagle.png"

filetitle=filename.split('.')[0]
start=datetime.datetime.now()
print("START: "+str(start))
print("ITERATIONS: "+str(iterations))
typavg=datetime.timedelta(seconds=39, milliseconds=166)
print("ESTIMATED TIME REMAINING: "+str(typavg*iterations))

#print(os.getcwd())
if plotAll is True:
    files=os.listdir("images/progression/")
    os.chdir("images/progression/")
    for j in files:
        os.remove(j)
    os.chdir("..")
    os.chdir("..")



"""
# generate a stock 2d numpy array, to be deleted later
# WARNING: uncommenting this section and running it will overwrite your paths.csv, possibly causing you to lose valuable previous path data...
# ...which would never ever happen to me because I'm brilliant and would never accidentally overwrite data...
init=np.array([[0,0],[999,0],[0,999],[999,999]])
with open(filetitle+'.csv', 'wb') as f:
    np.savetxt(f,init,fmt='%i',delimiter=',')
"""


paths=np.genfromtxt(filetitle+'.csv', delimiter=',',dtype=None)
startinglength=len(paths[:,0])

if iterations>0:
    for i in range(iterations):
        newpath=geodesic(filename,random.randint(0,999),random.randint(0,999),random.randint(0,999),random.randint(0,999),plotFig=False)
        paths=np.concatenate((paths, newpath), axis=0)
        print("LAP "+str(i+1)+": "+str(datetime.datetime.now()))
        print("CURRENT RUN TIME: "+str(datetime.datetime.now()-start))
        print("ESTIMATED TIME REMAINING: "+str(((datetime.datetime.now()-start)/(i+1))*(iterations-i-1)))
        with open(filetitle+'.csv', "wb") as f:
            np.savetxt(f,paths,fmt='%i',delimiter=',')
        if plotAll is True:
            plt.figure(figsize=(10, 10))
            plt.hist2d(paths[:,0], paths[:,1], bins=numbins)
            plt.subplots_adjust(bottom=0, top=1, left=0, right=1)
            ax=plt.gca()
            ax.axis("off")
            ax.invert_yaxis()
            ax.set_facecolor('xkcd:black')
            plt.hot()
            #plt.colorbar()
            plt.savefig('images/progression/'+str(i+1)+'.png')
            plt.close()

print("END: "+str(datetime.datetime.now()))
print("TOTAL RUN TIME: "+str(datetime.datetime.now()-start))
if iterations>0:
    print("AVG. TIME PER ITERATION: "+str((datetime.datetime.now()-start)/iterations))
print("STARTING # OF COORDINATES: "+str(startinglength))
print("CURRENT TOTAL # OF COORDINATES: "+str(len(paths[:,0])))
print("DIFFERENCE: "+str(len(paths[:,0])-startinglength))

plt.figure(figsize=(10, 10))
plt.hist2d(paths[:,0], paths[:,1], bins=numbins)
plt.subplots_adjust(bottom=0, top=1, left=0, right=1)
ax=plt.gca()
ax.axis("off")
ax.invert_yaxis()
#plt.gca().axis("off")
#plt.gca().invert_yaxis()
ax.set_facecolor('xkcd:black')
#plt.colorbar() # colorbar will ruin aspect ratio
plt.savefig('images/'+filename+' '+str(numbins)+'bins '+datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")+'.png',dpi=300)
plt.hot() # try viridis, plasma, inferno, magma, summer, bone, copper, pink, hot
plt.show()
