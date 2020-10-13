import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as mpl
#########################################
# Point cloud function starts here
#########################################
def p_cloud(d_image,K):
    # Inverting K so as P(U)=D(u)*K^-1*U
    K_inv=np.linalg.inv(K)
    point_cloud=[]
    # finding point clouds
    
    for loop1 in range(d_image.shape[0]):
        for loop2 in range(d_image.shape[1]):
            p_cl_tmp=d_image[loop1,loop2]*(np.dot(K_inv,[loop2,loop1,1]))
            if p_cl_tmp[0]!=0 or p_cl_tmp[1]!=0 or p_cl_tmp[2]!=0:
                point_cloud.append(p_cl_tmp)
    
    return np.asarray(point_cloud)

#########################################
# Point cloud function ends here
#########################################

#########################################
# Display the scatter plot of Images
#########################################

def display(p_cl1,p_cl2,color1,color2,img_name):
    fig = mpl.figure(figsize=(20,20))
    ax = fig.add_subplot(111, projection='3d')
    for loop in range(len(p_cl1)):
        ax.scatter(p_cl1[loop,0],p_cl1[loop,1],p_cl1[loop,2],s=9,c=color1,edgecolor=color1)
        #print loop
    
    for loop in range(len(p_cl2)):
        ax.scatter(p_cl2[loop,0],p_cl2[loop,1],p_cl2[loop,2],s=9,c=color2,edgecolor=color2)
    # The below commented section can be un commented to get rotated figure plot to compare with input
    for angle in range(0, 360):
       ax.view_init(270, angle)
    mpl.savefig('point_cloud'+img_name+'.jpg')
    mpl.show()
    mpl.close()
    return
#########################################
# Display the scatter plot of Images
#########################################
