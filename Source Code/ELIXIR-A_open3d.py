#!/usr/bin/env python
# coding: utf-8

# In[1]:

import numpy as np
import copy
import open3d as o3d
from biopandas.pdb import PandasPdb
import pdb_sphere
import jsontopdb
import sys


# In[2]:


#functions

#Step 1. Fast Point Feature Histogram feature calculation
def preprocess_point_cloud(pcd, voxel_size):
    #print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = pcd.voxel_down_sample(voxel_size)

    radius_normal = voxel_size * 2
    #print(":: Estimate normal with search radius %.3f." % radius_normal)
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

    radius_feature = voxel_size * 5
    #print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh

#Step 2. Downsample with a voxel size
#The input file is pharm_1 and pharm_2.
def prepare_dataset(voxel_size):
    #print(":: Load two point clouds and disturb initial pose.")
    source_1 = copy.deepcopy(pharm_1)
    target_1 = copy.deepcopy(pharm_2)
    trans_init = np.identity(4)
    
    source_1.transform(trans_init)
    source_down, source_fpfh = preprocess_point_cloud(source_1, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target_1, voxel_size)
    return source_1, target_1, source_down, target_down, source_fpfh, target_fpfh

#Step 3. Global registration with RANSAC iteration
def execute_global_registration(source_down, target_down, source_fpfh,
                                target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    #print(":: RANSAC registration on downsampled point clouds.")
    #print("   Since the downsampling voxel size is %.3f," % voxel_size)
    #print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        3, [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold)
        ], o3d.pipelines.registration.RANSACConvergenceCriteria(400000,500))
    return result

#Step 4. Downsample with a voxel size and Estimate normal with k-d tree
def downsample_Estimate_kdtree(source,radius):
    source_down = source.voxel_down_sample(radius)
    source_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius * 2, max_nn=30))
    return source_down

def color_pharm(sourceipc):
    shortlist=['HDR','HAC','HPB','PIO','NIO','ARO']
    colorlist=[[0,1,1],[1,0,0],[0,0,1],[1,0,1],[1,1,0],[0,1,0],[0,0,0]]
    color_out=[]
    for i in range(len(sourceipc)):
        for j in range(len(shortlist)):
            if sourceipc[i]==shortlist[j]:
                for t in range(1000):
                    color_out.append(colorlist[j])
            if sourceipc[i] not in shortlist:
                for t in range(1000):
                    color_out.append(colorlist[-1])
    return np.array(color_out)
    


# In[3]:


data0 = sys.argv[1] #file path 1
data1 = sys.argv[2] #file path 2
data2 = sys.argv[3] #g_voxel
data3 = sys.argv[4] #iteractions
data4 = sys.argv[5] #relative_fitness
data5 = sys.argv[6] #relative_rmse
data6 = sys.argv[7] #correspondence distance


# In[3]:


# data0='/Users/haoqi/Desktop/open3d_test/Dengue_RdRp/5I3P.json'
# data1='/Users/haoqi/Desktop/open3d_test/Dengue_RdRp/5I3Q.json'


# In[4]:


# data2 = 0.8 #voxel size
# data3 = 100 #iteractions
# data4 = 0.1 #relative_fitness
# data5 = 0.1 #relative_rmse


# In[5]:


import logging
logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)


# In[6]:


if len(data0)>4 and data0[-4:]=='json':
    jsontopdb.exportpdbdata(data0)
    data0pdb= data0 + '.pdb'
    #data0+='.pdb'
elif len(data0)>3 and data0[-3:]=='pdb':
    data0pdb= data0


if len(data1)>4 and data1[-4:]=='json':
    jsontopdb.exportpdbdata(data1)
    #data1+='.pdb'
    data1pdb= data1 + '.pdb'
elif len(data1)>3 and data1[-3:]=='pdb':
    data1pdb= data1

source_input = PandasPdb().read_pdb(data0pdb)
target_input = PandasPdb().read_pdb(data1pdb)


# In[7]:



source_input_xyz = source_input.df['ATOM'].loc[:,['x_coord','y_coord','z_coord']]
source_input_occ = source_input.df['ATOM'].loc[:,['occupancy']].to_numpy()
source_input_pha = source_input.df['ATOM'].loc[:,['residue_name']].to_numpy()
source_input_np=source_input_xyz.to_numpy()

target_input_xyz = target_input.df['ATOM'].loc[:,['x_coord','y_coord','z_coord']]
target_input_occ = target_input.df['ATOM'].loc[:,['occupancy']].to_numpy()
target_input_pha = target_input.df['ATOM'].loc[:,['residue_name']].to_numpy()
target_input_np=target_input_xyz.to_numpy()



print("High accuracy mode")

result_ransac_li=[]
result_cicp_li=[]
result_cicp_fi=[]
#source_input_np_clouds=pdb_sphere.pdb_to_sphere(source_input_np,source_input_occ)
#target_input_np_clouds=pdb_sphere.pdb_to_sphere(target_input_np,target_input_occ)
for loop in range(5):
    source_input_np_clouds=pdb_sphere.pdb_to_sphere(source_input_np,source_input_occ)
    target_input_np_clouds=pdb_sphere.pdb_to_sphere(target_input_np,target_input_occ)

    pharm_1 = o3d.geometry.PointCloud()
    pharm_1.points = o3d.utility.Vector3dVector(source_input_np_clouds)
    pharm_1.paint_uniform_color([1, 0.706, 0])


    pharm_2 = o3d.geometry.PointCloud()
    pharm_2.points = o3d.utility.Vector3dVector(target_input_np_clouds)
    pharm_2.paint_uniform_color([1, 0.706, 0])

    colored_residue= True
    if colored_residue:
        pharm_1.colors=o3d.utility.Vector3dVector(color_pharm(source_input_pha))
        pharm_2.colors=o3d.utility.Vector3dVector(color_pharm(target_input_pha))


    voxel_size = float(data2)
    pharm_1_global, pharm_2_global, pharm_1_down,pharm_2_down, pharm_1_fpfh, pharm_2_fpfh = prepare_dataset(voxel_size)


    result_ransac = execute_global_registration(pharm_1_down, pharm_2_down,
                                                pharm_1_fpfh, pharm_2_fpfh,
                                                voxel_size)
    #print("Now performing global registration.")
    #print(result_ransac)

    pharm_1.transform(result_ransac.transformation)
    pharm_1_cicp = downsample_Estimate_kdtree(pharm_1,voxel_size)
    pharm_2_cicp = downsample_Estimate_kdtree(pharm_2,voxel_size)

    if not pharm_1_cicp.colors:
        pharm_1_cicp.paint_uniform_color([1, 0.706, 0])
        print("Colored icp is not applicable to the first pharmacophores. Running the normal ICP algorithm.")
    if not pharm_2_cicp.colors:
        pharm_2_cicp.paint_uniform_color([1, 0.706, 0])
        print("Colored icp is not applicable to the second pharmacophores. Running the normal ICP algorithm.")



    #print("Now performing colored icp registration.")
    iters = int(data3)
    r_fitness = float(data4)
    r_rmse = float(data5)

    result_cicp=""
    current_transformation = np.identity(4)

    extend_colored_icp=False

    try:
        result_cicp = o3d.pipelines.registration.registration_colored_icp(
                pharm_1_cicp, pharm_2_cicp, voxel_size, current_transformation,
                o3d.pipelines.registration.TransformationEstimationForColoredICP(),
                o3d.pipelines.registration.ICPConvergenceCriteria(relative_fitness=r_fitness,
                                                                  relative_rmse=r_rmse,
                                                                  max_iteration=iters))
        #print(result_cicp)
    except RuntimeError:
        extend_colored_icp=True
        pass
    
    
    if result_cicp:
        result_ransac_li.append(result_ransac)
        result_cicp_li.append(result_cicp)
        result_cicp_fi.append(round(result_cicp.fitness,3))
        #print("The fitness ratio of colored ICP is ",round(result_cicp.fitness,3)*100,"%.", sep = '')
    
#Find the best match
if len(result_ransac_li) == len(result_cicp_li):
    result_cicp=result_cicp_li[result_cicp_fi.index(max(result_cicp_fi))]
    result_ransac=result_ransac_li[result_cicp_fi.index(max(result_cicp_fi))]
    #print("Possible registrations were found with the following values:",result_cicp_fi)
    
    
    
while not result_cicp:
    try:
        #print(result_cicp)
        #print("loop",r_rmse)
        result_cicp = o3d.pipelines.registration.registration_colored_icp(
                pharm_1_cicp, pharm_2_cicp, voxel_size, current_transformation,
                o3d.pipelines.registration.TransformationEstimationForColoredICP(),
                o3d.pipelines.registration.ICPConvergenceCriteria(relative_fitness=r_fitness,
                                                                  relative_rmse=r_rmse,
                                                                  max_iteration=iters))
        #print(result_cicp)
        #print("loop",r_rmse)
    except RuntimeError:
        r_fitness*=10
        r_rmse*=10
    if r_fitness>1000:
        break
    elif r_rmse>1000:
        break
if extend_colored_icp == True:
    if not result_cicp:
        print("No overlaid pharmacophore found through colored ICP.")
        print(r_fitness,r_rmse)
    else:
        print(result_cicp)


        
        


source_np_plot=copy.deepcopy(source_input_np)

source_plot = o3d.geometry.PointCloud()
source_plot.points= o3d.utility.Vector3dVector(source_np_plot)

target_plot = o3d.geometry.PointCloud()
target_plot.points= o3d.utility.Vector3dVector(target_input_np)

source_plot.transform(result_ransac.transformation)
if result_cicp:
    if result_cicp.fitness != 0:
        source_plot.transform(result_cicp.transformation)

print("Now performing global registration.")
print(result_ransac)
print("Now performing colored icp registration.")
print(result_cicp)
        

print("The fitness ratio of RANSAC registration is ",round(result_ransac.fitness*100,3),"%.", sep = '')
print("The fitness ratio of colored ICP is ",round(result_cicp.fitness*100,3),"%.", sep = '')
print("The output file is saved in the same folder as the input file.")



distance_threshold = float(data6) # Select the point pairs within input value.

Source_linked=[]
for source_index in range(len(source_plot.points)):
    for targets in target_input_np:
        distance = np.linalg.norm(targets - np.array(source_plot.points[source_index]))
        if distance <= distance_threshold:
            Source_linked.append(source_index)
            break


Target_linked=[]
for targets in range(len(target_input_np)):
    for source_index in range(len(source_plot.points)):
        distance = np.linalg.norm(target_input_np[targets] - np.array(source_plot.points[source_index]))
        if distance <= distance_threshold:
            
            Target_linked.append(targets)
            break



source_output = copy.deepcopy(source_input)
source_output.df['ATOM'].loc[:,['x_coord','y_coord','z_coord']]=np.array(source_plot.points)
source_output.df['ATOM']=source_output.df['ATOM'].loc[Source_linked,:]

target_output = copy.deepcopy(target_input)
target_output.df['ATOM'].loc[:,['x_coord','y_coord','z_coord']]=np.array(target_input_np)
target_output.df['ATOM']=target_output.df['ATOM'].loc[Target_linked,:]


# In[25]:


source_output.to_pdb(path=data0+'_source_out.pdb')
target_output.to_pdb(path=data1+'_target_out.pdb')

# In[ ]:




