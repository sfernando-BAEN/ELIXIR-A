
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


#test case
s='ATOM     12  C2  IPROA  12      10.500   8.000   9.000  0.75 -1.20           C'
dim=[ -2.94243362,  -7.04664655, -19.21504611]
# s='ATOM   3879  HB  ILE P 275      -4.634  12.246  -2.478  1.00  0.00      P1   H'


def dimtopdb(dim,ori,gaptype=1):
    Sl = re.split(r'[ ]{1,999}', ori)
    for i in range(len(dim)):
        dim[i]=str(round(dim[i],3))
        Sl[i+gaptype+4]=dim[i]
    new=''

    if gaptype == 1:
        gap = [4, 7, 4, 7, 4, 12, 8, 8, 6, 6, 12]  # 5,6,7 are coors
    elif gaptype == 2:
        gap = [4, 7, 4, 5, 2, 4, 12, 8, 8, 6, 6, 8, 4] #6,7,8 are coors

    for i in range(len(Sl)):
        new+=Sl[i].rjust(gap[i])
    return new


if __name__ == '__main__':

    print(dimtopdb(dim,s))
    print(s)