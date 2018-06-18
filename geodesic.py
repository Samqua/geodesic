# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 20:02:42 2018

@author: Samqua

Discrete geodesic solver using shortest path algorithms from the networkx package.
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime
import random

def geodesic(terrain,x0,y0,x1,y1,treatData=False,treatFunction=lambda x:x,returnLength=False,plotFig=True,imagesize=8,savePlot=False):
    
    """
    Discrete geodesic solver using shortest path algorithms from the networkx package.
    Specify a square terrain matrix, the source coordinates (x0,y0), and the target coordinates (x1,y1).
    We employ the convention that the origin is (0,0), i.e. the bottom leftmost element of the terrain matrix is the origin.
    N.B. the plt.imread() function is
    """
    
    if isinstance(terrain, str) is True:
        try:
            if ".png" in terrain:
                data=plt.imread(terrain,"PNG") # incorrect structure
                data=np.transpose(data) # correct structure
            elif ".jpg" in terrain:
                data=plt.imread(terrain,"JPG") # incorrect structure
                data=np.transpose(data) # correct structure
            else:
                print("Error: image file is not a PNG or JPG.")
                return 0
        except FileNotFoundError:
            print("Error: "+terrain+" file not found...")
            return 0
    elif isinstance(terrain,list) is True:
        data=np.array(terrain)
    elif isinstance(terrain,numpy.ndarray) is True:
        data=terrain
    else:
        print("Error: input data is not an image file, list of lists, or numpy array.")
        return 0
    
    if len(data)!=len(np.transpose(data)):
        print("Error: terrain is not a square matrix.")
    else:
        if treatData is True:
            treatFunction=np.vectorize(treatFunction)
            data=treatFunction(data)
        n=len(data)
        labelsdict={}
        def labels(i,j): # assigns a unique label to every point in the n by n lattice... counts horizontally (y=j=0) first, and then increases (downwards) in the +y (j) direction
            return n*j+(i%n)
        for i in range(n):
            for j in range(n):
                labelsdict[labels(i,j)]=[i,j] # in labelsdict, the key is the label labels(i,j), while the value is the coordinate pair [i,j]
                # in other words, to get the label from the coordinates, use labels(i,j), while to get the coordinates from the label, use lablesdict[label]
        def makeLattice(sidelength): # returns a dictionary such that the key is a lattice point label and the value is a list of labels of nodes in the key label's Moore neighborhood
            g={}
            for i in range(sidelength):
                for j in range(sidelength):
                    g[labels(i,j)]=[]
            for i in range(sidelength):
                for j in range(sidelength):
                    if (j+1)<sidelength:
                        g[labels(i,j)].append(labels(i,j+1))
                    if (j-1)>=0:
                        g[labels(i,j)].append(labels(i,j-1))
                    if (i-1)>=0:
                        g[labels(i,j)].append(labels(i-1,j))
                        if (j-1)>=0:
                            g[labels(i,j)].append(labels(i-1,j-1))
                        if (j+1)<sidelength:
                            g[labels(i,j)].append(labels(i-1,j+1))
                    if (i+1)<sidelength:
                        g[labels(i,j)].append(labels(i+1,j))
                        if (j-1)>=0:
                            g[labels(i,j)].append(labels(i+1,j-1))
                        if (j+1)<sidelength:
                            g[labels(i,j)].append(labels(i+1,j+1))
            return g
        graph=nx.from_dict_of_lists(makeLattice(n))
        def weight(source,target): # return weight of connection from node i to node j; from terrain
            return math.sqrt((labelsdict[target][0]-labelsdict[source][0])**2+(labelsdict[target][1]-labelsdict[source][1])**2+(int(data[labelsdict[source][0]][labelsdict[source][1]])-int(data[labelsdict[target][0]][labelsdict[target][1]]))**2) # distance formula
        for x in graph.edges:
            graph[x[0]][x[1]]['weight']=weight(x[0],x[1]) # add weights to networkx graph
        # trajectory as np array
        traj=np.array([labelsdict[x] for x in nx.shortest_path(graph,labels(x0,y0),labels(x1,y1),weight='weight')]) # much faster than dijkstra somehow?
        if plotFig is True:
            plt.figure(figsize=(imagesize,imagesize))
            plt.matshow(np.transpose(data),fignum=1)
            plt.plot(traj[:,0],traj[:,1],color="red")
            if savePlot is True:
                plt.savefig('images/'+'geodesic '+datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")+'.png',bbox_inches='tight')
        if returnLength is False:
            return traj 
        else:
            return [nx.shortest_path_length(graph,labels(x0,y0),labels(x1,y1),weight='weight'),traj]