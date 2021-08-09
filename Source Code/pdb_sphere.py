#!/usr/bin/env python
# coding: utf-8

# In[1]:


from numpy import pi, cos, sin, arccos, arange
#import mpl_toolkits.mplot3d
#import matplotlib.pyplot as pp
import numpy as np
import copy
import open3d as o3d
from biopandas.pdb import PandasPdb


def dot_sphere(x0,y0,z0,occupancy=0.5, num_pts=1000):
    num_pts = 1000
    #num_pts = round((10*occupancy)**3)
    angle1=np.random.random(num_pts)*2*pi;
    angle2=arccos(np.random.random(num_pts)*2-1);
    r=np.random.random(num_pts)**(1/3)*occupancy;
    x=r*cos(angle1)*sin(angle2);
    y=r*sin(angle1)*sin(angle2);
    z=r*cos(angle2);
    x=x+x0;
    y=y+y0;
    z=z+z0
    return np.array([x,y,z]).T
# pp.figure().add_subplot(111, projection='3d').scatter(x,y,z);
# pp.show()


def pdb_to_sphere(pdbdots,occupancy):
    pdb_out=""
    for i in range(len(pdbdots)):
        if i == 0:
            pdb_out=dot_sphere(pdbdots[i,0],pdbdots[i,1],pdbdots[i,2],np.ndarray.item(occupancy[i]))
        else:
            pdb_out = np.concatenate((pdb_out,dot_sphere(pdbdots[i,0],pdbdots[i,1],                                                         pdbdots[i,2],np.ndarray.item(occupancy[i]))), axis=0)
    return pdb_out





