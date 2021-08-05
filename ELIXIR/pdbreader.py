#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Author: Haoqi Wang
"""
import numpy as np
import re

def extract(filename):
    with open(filename) as file:
        data=file.readlines()
        mat=[]
        for i in data:
            spl=re.split(r'[ ]{1,999}',i)
            if spl[0]=="REMARK":
                continue
            elif spl[0]=="ATOM":
                #cases of Protein and Ligand ABC
                if re.findall(r'[a-zA-Z]{1,999}',spl[4]):
                    mat += [[float(spl[6]), float(spl[7]), float(spl[8])]]
                else:
                    mat+=[[float(spl[5]),float(spl[6]),float(spl[7])]]
            else:
                continue
        mat=np.array(mat)
    return mat

def dimtopdb(dim,ori,num=0,gaptype=1):
    Sl = re.split(r'[ ]{1,999}', ori)
    Sl[4]=str(num)
    for i in range(len(dim)):
        dim[i]=str(round(dim[i],3))
        Sl[i+gaptype+4]=dim[i]

    new=''

    if gaptype == 1:
        gap = [4, 7, 4, 7, 4, 12, 8, 8, 6, 6, 12]  # 5,6,7 are coors
    elif gaptype == 2:
        gap = [4, 7, 5, 4, 2, 4, 12, 8, 8, 6, 6, 8, 4] #6,7,8 are coors

    for i in range(len(Sl)):
        Sl=list(map(str,Sl))
        new+=Sl[i].rjust(gap[i])

    return new

def rewrite(filename,defaultoutput,input):
    if len(input)!=len(defaultoutput):
        print("The matrix doesn't match the default pdb file. Please try it again later.")
        return
    d=defaultoutput
    with open(filename) as file:
        data=file.readlines()
        mat=[]
        count=0
        matrixcount=0
        for i in data:
            spl=re.split(r'[ ]{1,999}',i)
            if spl[0]=="REMARK":
                continue
            elif spl[0]=="ATOM":
                # print('Before change:',data[count])
                #cases of Protein and Ligand ABC
                if re.findall(r'[a-zA-Z]{1,999}',spl[4]): #define the pdb type
                    data[count]=dimtopdb(input[matrixcount], i, gaptype=2)
                else:
                    data[count]=dimtopdb(input[matrixcount], i, gaptype=1)
                print("After change",data[count])
                matrixcount += 1
            else:
                continue
            count+=1

        newname=filename[:-4]+'_new.pdb'
        with open(newname,'w') as f:
            for i in data:
                f.write(i)
        print('Done')



if __name__ == '__main__':
    pass
    # test case
    s = 'ATOM      1  C2  IPROA  99      10.500   8.000   9.000  0.00  0.00           C'
    dim = [-2.94243362, -7.04664655, -19.21504611]
    print(dimtopdb(dim,s))
    print(s)
    # C=extract("./data/O104_site_3.pdb")
    # print(C)
