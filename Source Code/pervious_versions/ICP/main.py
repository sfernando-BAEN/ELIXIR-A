"""

Author: Vishveswaran Jothi
"""

import numpy as np
import matplotlib.pyplot as mpl
import pc1 
import icp1
import time
#from mpl_toolkits.mplot3d import Axes3D
##########################################
# Input from the user to Load the txtfiles
##########################################
"""
path_prompt = "Enter the full path for the text files:"
img_name_prompt = "Enter the text file name with file extension:"
max_iter_prompt = "Enter the max iteration for matching the point clouds"
k_prompt="Enter the intrinsic parameter matrix"
threshold_prompt = "Enter the Threshold for matching correspondence"

path1=raw_input(">"+path_prompt)
img_name1=raw_input(">"+img_name_prompt)
max_iter=raw_input(">"+max_iter_prompt)
path2=raw_input(">"+path_prompt)
img_name2=raw_input(">"+img_name_prompt)
print k_prompt
K=np.zeros((3,3),dtype='int')
for loop in range(3):
    for loop1 in range(3):
        K[loop,loop1]=int(raw_input("> Enter the element"+[loop,loop1]+": "))
threshold=int(raw_input(">"+threshold_prompt))
"""
#########################################

#########################################
# Sample input from user
#########################################

path="./"
img_name1="depthImage1ForHW.txt"
img_name2="depthImage2ForHW.txt"
max_iter=23
K=np.array([[365,0,256],[0,365,212],[0,0,1]])
threshold=0.01

#########################################
# Algorithm starts here
#########################################
d_image1=np.loadtxt(path+"/"+img_name1)
d_image2=np.loadtxt(path+"/"+img_name2)
img_name1=img_name1.split('.')[0]
img_name2=img_name2.split('.')[0]
#cv2.imwrite('disp_'+img_name1.split('.')[0]+'.jpg',255*d_image1)
#cv2.imwrite('disp_'+img_name2.split('.')[0]+'.jpg',255*d_image2)

#create as a depth color image for Image 1
mpl.figure()
mpl.imshow(d_image1,origin='upper',extent=[0, d_image1.shape[1], 0, d_image1.shape[0]])
mpl.colorbar()
# Save the colored depth image
mpl.savefig('op_1'+img_name1+'.jpg')
#mpl.close()
#create as a depth color image for Image 2
mpl.figure()
mpl.imshow(d_image2,origin='upper',extent=[0, d_image2.shape[1], 0, d_image2.shape[0]])
mpl.colorbar()
# Save the colored depth image
mpl.savefig('op_1'+img_name2+'.jpg')
mpl.show()
#mpl.close()

##################################################
# Plot before ICP function
#################################################
# creating the point clouds
point_cloud_img1=pc1.p_cloud(d_image1,K)
point_cloud_img2=pc1.p_cloud(d_image2,K)
"""
img_name="_before_ICP"
print "The output is saved in point_cloud"+img_name+".jpg"
pc1.display(point_cloud_img1,point_cloud_img2,'b','g',img_name)
print " Running ICP algorithm..."
"""
##################################################
# ICP function
#################################################
#time.sleep(5)
pt_cl_2_trans=icp1.icp_alg(point_cloud_img1,point_cloud_img2,max_iter,threshold)
print " Plotting the result of ICP algorithm..."

##################################################
# Plot after ICP function
#################################################

img_name="_after_ICP_T_0.01_var23"
print "The output is saved in point_cloud"+img_name+".jpg"
pc1.display(point_cloud_img1,pt_cl_2_trans,'b','r',img_name)

