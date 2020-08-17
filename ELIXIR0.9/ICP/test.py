#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdbreader
import icp1
import time
import figureplot
from numpy import *

#default parameters.
max_iter=101
threshold=100

#
#pathofpA='./data/O104_site_2_soln_3.pdb' #case 1
#pathofpB='./data/PBP_site_1_soln_5.pdb'

# pathofpA='./data/O104_site_3.pdb' #case 2
# pathofpB='./data/PBP_site_1.pdb'
# #
# pathofpA='./data/blactmaseO104.pdb' #case 3
# pathofpB='./data/1hvb_p.pdb'

###import from ELIXIR-A.tcl
import sys

print "This is the name of the script: ", sys.argv[0]
print "Number of arguments: ", len(sys.argv)
print "The arguments are: " , str(sys.argv)

Input = sys.argv[1]
data=Input.split(" ")
print data
data=map(float,data)
print data

#data is 5x5
pA=[];pB=[]
for i in range(len(data)//6):
    tmp=[data[3*i],data[3*i+1],data[3*i+2]]
    if tmp != [0,0,0]:
        pA.append(tmp)
    else:
        break
print "pA",pA
for i in range(len(data)//6,len(data)//3):
    tmp=[data[3*i],data[3*i+1],data[3*i+2]]
    if tmp != [0,0,0]:
        pB.append(tmp)
    else:
        break
print "pB",pB

#pA,pB=pdbreader.extract(pathofpA),pdbreader.extract(pathofpB)

# print pA

pA_unsorted=pA

pA_index=c_[pA,array(range(len(pA)))]
pB_index=c_[pB,array(range(len(pB)))]

pA_index_sorted=pA_index[argsort(pA_index[:, 0])]
pB_index_sorted=pB_index[argsort(pB_index[:, 0])]

# print(pA_index,pA_index_sorted)


pA_sorted=pA_index_sorted[:,0:3]
pB_sorted=pB_index_sorted[:,0:3]
# print(pA_sorted)
#
figureplot.plot_icp2(pA_sorted,pB_sorted,'./figures/initial_plot+'+'-'.join(time.ctime().split(' ')[1:]))
#
#
#
pt_cl_2_trans=icp1.icp_alg(pA_sorted,pB,max_iter,threshold)
#
# print('The result:',pt_cl_2_trans)
# print(pA)


def distance(clusterA,clusterB):

    d=[2147483648]*len(clusterA)
    for iA in range(len(clusterA)):
        for iB in range(len(clusterB)):
            d[iA]=min(d[iA],sum([(float(clusterA[iA][i])-float(clusterB[iB][i]))**2 for i in [0,1,2]])**0.5)
    return d

print("the originaldistance is ",distance(pA,pB))
print("the distance is ",distance(pA,pt_cl_2_trans))
# pdbreader.rewrite(pathofpB,pB,pt_cl_2_trans)
#
# # flann = FLANN()
# # result,dists = flann.nn(pA,pB,5,algorithm="kmeans",branching=32, iterations=8, checks=16);
#
#
# print result,size(result)
# print dists,size(dists)
