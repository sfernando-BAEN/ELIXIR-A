#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdbreader
import icp1
import time
#import figureplot
from numpy import *
import sys


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

#print "This is the name of the script: ", sys.argv[0]
#print "Number of arguments: ", len(sys.argv)
#print "The arguments are: " , str(sys.argv)

data0 = sys.argv[1] #length of phar 1
data1 = sys.argv[2] #occupation of phar 1
data2 = sys.argv[3] #length of phar 2
data3 = sys.argv[4] #occupation of phar 2
data4 = sys.argv[5] #data of phar 1
data5 = sys.argv[6] #data of phar 2
data6 = sys.argv[7] #data of path
#data7 = sys.argv[8]
#print data0

#ph1
numph1=data0
#tmp=data0[1].split(" ")
data1=data1[1:-1].split(" ")
occph1=[i for i in range(len(data1)) if data1[i]=="1"]
data4=data4.split(" ")[1:]
pA0=[]
for ind in occph1:
    tmp=[]
    for element in data4[ind].split(","):
        tmp.append(element)
    pA0.append(tmp)
pA0=array(pA0)
pA=pA0[:,[2,3,4]]
pA=pA.astype(float)
for i in range(len(pA)):
    if pA[i,0]==0 and pA[i,1]==0 and pA[i,2]==0:
        pA[i,2]=0.0000000001
print pA
#ph2
data3=data3[1:-1].split(" ")
occph2=[i for i in range(len(data3)) if data3[i]=="1"]
data5=data5.split(" ")[1:]
pB0=[]
for ind in occph2:
    tmp=[]
    for element in data5[ind].split(","):
        tmp.append(element)
    pB0.append(tmp)
pB0=array(pB0)
pB=pB0[:,[2,3,4]]
pB=pB.astype(float)
for i in range(len(pB)):
    if pB[i,0]==0 and pB[i,1]==0 and pB[i,2]==0:
        pB[i,2]=0.00000000001
        print "changed"
print pB
#data=Input.split(" ")
##print data
#data=map(float,data)
##print data
#
##data is 5x5
#pA=[];pB=[]
#for i in range(len(data)//6):
#    tmp=[data[3*i],data[3*i+1],data[3*i+2]]
#    if tmp != [0,0,0]:
#        pA.append(tmp)
#    else:
#        break
##print "pA",pA
#for i in range(len(data)//6,len(data)//3):
#    tmp=[data[3*i],data[3*i+1],data[3*i+2]]
#    if tmp != [0,0,0]:
#        pB.append(tmp)
#    else:
#        break
#if pA==pB and len(pA)==0:
#    print "No data was received from the form. Please sumbit it again!"
##print "pB",pB
#else:
#    print "ELXIR-A starts to merge two clusters."
#pA=array(pA)
#pB=array(pB)
#
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
#figureplot.plot_icp2(pA_sorted,pB_sorted,'./figures/initial_plot+'+'-'.join(time.ctime().split(' ')[1:]))
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

dist=distance(pA,pt_cl_2_trans)

def Sortpoints(distpoints):
    if len(sorted(distpoints))<5:
        return [distpoints.index(sorted(distpoints)[i]) for i in range(len(distpoints))]
    elif len(sorted(distpoints)[:5])==len(set(sorted(distpoints)[:5])):
        return [distpoints.index(sorted(distpoints)[i]) for i in range(len(distpoints))]
    else:
        tmp=[]
        stmp=sorted(distpoints)[:4]
        for i in stmp:
            for j in range(len(distpoints)):
                if i==distpoints[j]:
                    tmp.append(j)
    return tmp[:]

def guesstype(A,B):
    if A==B:
        return A
    else:
        return A+"/"+B



print "the original distance is "
print distance(pA,pB)
print "the treated distance is "
print distance(pA,pt_cl_2_trans)
print len(distance(pA,pt_cl_2_trans))
print "\n-----------------------------------------------------------------------"

Sori=Sortpoints(distance(pA,pt_cl_2_trans))
Sicp=Sortpoints(distance(pt_cl_2_trans,pA))


outputfile=['{\n', '    "points": [\n']
outputpdb=[]
timer=1
s = 'ATOM      1  C2  XXXXX  99      10.500   8.000   9.000  0.00  0.00           C\n'
fragment1=['        {\n', '            "name": "', '            "hasvec": false,\n', '            "x":', '            "y":', '            "z":', '            "radius": 1,\n', '            "enabled": true,\n', '            "vector_on": 0,\n', '            "svector": {\n', '                "x": 1,\n', '                "y": 0,\n', '                "z": 0\n', '            },\n', '            "minsize": "",\n', '            "maxsize": "",\n', '            "selected": true\n', '        }']
fragment2=['    ],\n', '    "subset": "molport",\n', '    "ShapeModeSelect": "filter",\n', '    "inselect": "none",\n', '    "intolerance": 1,\n', '    "inshapestyle": "inshapestyle-solid",\n', '    "exselect": "none",\n', '    "extolerance": 1,\n', '    "exshapestyle": "exshapestyle-solid",\n', '    "max-orient": "",\n', '    "reduceConfs": "",\n', '    "max-hits": "",\n', '    "minMolWeight": "",\n', '    "maxMolWeight": "",\n', '    "minrotbonds": "",\n', '    "maxrotbonds": "",\n', '    "minlogp": "",\n', '    "maxlogp": "",\n', '    "minpsa": "",\n', '    "maxpsa": "",\n', '    "minaromatics": "",\n', '    "maxaromatics": "",\n', '    "minhba": "",\n', '    "maxhba": "",\n', '    "minhbd": "",\n', '    "maxhbd": "",\n', '    "LigandMolStyleSelect": "stick",\n', '    "LigandMolStyleSelectcolor": "#c8c8c8",\n', '    "ResultsMolStyleSelect": "stick",\n', '    "ResultsMolStyleSelectcolor": "#808080",\n', '    "ReceptorMolStyleSelect": "cartoonwire",\n', '    "ReceptorMolStyleSelectcolor": "#c8c8c8",\n', '    "receptorbackbone": "plainBackbone",\n', '    "surfaceopacity": 0.8,\n', '    "backgroundcolor": "whiteBackground",\n', '    "ligand": null,\n', '    "ligandFormat": null,\n', '    "receptor": null,\n', '    "recname": null,\n', '    "receptorid": null,\n', '    "view": [\n', '        0,\n', '        0,\n', '        0,\n', '        18.873262406249992,\n', '        0.6300778787272721,\n', '        0.08411783594121802,\n', '        0,\n', '        -0.7719624708592429\n', '    ]\n', '}']

print "The overlapped pharmacospheres (top 5) in group 1 (original selected coordinate)"

for i in range(min(len(Sori),10)):
    # print pt_cl_2_trans[i]
    print "Name: ",pA0[Sori[i],0],"Type: ",pA0[Sori[i],1],"X:",round(pA[Sori[i]][0],3),"Y:",round(pA[Sori[i]][1],3),"Z:",round(pA[Sori[i]][2],3)
print "The overlapped pharmacospheres (top 5) in group 2 (transformed coordinate)"

for i in range(min(len(Sicp),10)):
    # print pt_cl_2_trans[i]
    print "Name: ",pB0[Sicp[i],0],"Type: ",pB0[Sicp[i],1],"X:",round(pt_cl_2_trans[Sicp[i]][0],3),"Y:",round(pt_cl_2_trans[Sicp[i]][1],3),"Z:",round(pt_cl_2_trans[Sicp[i]][2],3)


print "The overlapped pharmacospheres in group 3 (preferred average coordinate based on 1 and 2)"
for i in range(min(20,min(len(pt_cl_2_trans),len(Sori)))):
    tmpA=0.5*(pt_cl_2_trans[Sicp[i]][0]+pA[Sori[i]][0])
    tmpB=0.5*(pt_cl_2_trans[Sicp[i]][1]+pA[Sori[i]][1])
    tmpC=0.5*(pt_cl_2_trans[Sicp[i]][2]+pA[Sori[i]][2])
#    tmpA=round(pt_cl_2_trans[Sicp[i]][0],3)
#    tmpB=round(pt_cl_2_trans[Sicp[i]][1],3)
#    tmpC=round(pt_cl_2_trans[Sicp[i]][2],3)
#    print "Type: ",guesstype(pA0[Sori[i],1],pB0[Sicp[i],1]),"X:",round(tmpA,3),"Y:",round(tmpB,3),"Z:",round(tmpC,3)
    print "Name: ",guesstype(pA0[Sori[i],0],pB0[Sicp[i],0]),"X:",round(tmpA,3),"Y:",round(tmpB,3),"Z:",round(tmpC,3)


    f = fragment1[:]
    f[1] += pA0[Sori[i], 1] + "\",\n"
    f[3] += str(round(tmpA, 3)) + ",\n"
    f[4] += str(round(tmpB, 3)) + ",\n"
    f[5] += str(round(tmpC, 3)) + ",\n"
    f[-1]="        },\n"

    for j in f:
        outputfile.append(j)
    outputpdb.append(pdbreader.dimtopdb([round(tmpA,3),round(tmpB,3),round(tmpC,3)],s,num=timer))
    timer+=1


# ATOM      7  C2  XXXXX   7       9.000   2.000  12.000  0.00  0.00           C

outputfile[-1]="        }\n"
for k in fragment2:
    outputfile.append(k)
outputpath = ""
outputpdbpath = ""
if data6=="":
    outputpath="pharmit.json"
    outputpdbpath = "output.pdb"
else:
    outputpath=data6+"/"+"pharmit.json"
    outputpdbpath = data6+"/"+"output.pdb"
output=open(outputpath,'w+')
for lines in outputfile:
    output.write(lines)
output.close()
print "The pharmit session file has been writen as pharmit.json."

output=open(outputpdbpath,'w+')
for lines in outputpdb:
    output.write(lines)
output.close()
print "The pdb file has been writen as output.pdb."
