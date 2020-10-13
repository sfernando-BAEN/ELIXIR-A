import numpy as np
import figureplot
import time

#########################################
# ICP algorithm starts here
#########################################
def icp_alg(p_cl1,p_cl2,max_iter,threshold):
    default=(p_cl1,p_cl2)
    for iter in range(max_iter):
        # Printing the iteration count
        # print iter
        # Finding the correspondence with euclidean distance
        p_cl1_d,p_cl2_d= Corres(p_cl1,p_cl2,threshold)
        if p_cl2_d==[]:
            print "No matches were found"
            return p_cl2_d
        # Now calculate the centroid for each image
        N=len(p_cl1_d)
        # print p_cl1_d.shape,p_cl2_d.shape
        # print p_cl1_d,p_cl2_d
        if iter//100==iter/100.0 and iter>0:
            fname='./figures/icp with '+str(iter)+' time(s) of iteration(s)'+'-'.join(time.ctime().split(' ')[1:])
            figureplot.plot_icp(default[0],p_cl2,fname)
            figureplot.plot_icp3(default[0],p_cl2,default[1],fname)
            # print default[1]
        # finding centroid
        p_centroid=np.array([sum(p_cl1_d[:,0]),sum(p_cl1_d[:,1]),sum(p_cl1_d[:,2])])/(N)
        q_centroid=np.array([sum(p_cl2_d[:,0]),sum(p_cl2_d[:,1]),sum(p_cl2_d[:,2])])/(N)
        # print p_centroid,q_centroid
        
        # Now calculate resulting point clouds
        Mp=np.subtract(p_cl1_d,p_centroid)
        Mq=np.subtract(p_cl2_d,q_centroid)
        C=np.dot(Mq.T,Mp)
        # to find the rotation and translation between the images
        U,sig,Vt=np.linalg.svd(C)
        Rot_mat_tmp=np.dot(U,Vt)
        Rot_mat=Rot_mat_tmp.T
        # obtain the translation by P_centroid-R*q_centroid
        trans_vec=p_centroid-np.dot(Rot_mat,q_centroid)
        tfm_mat=np.zeros((4,4),dtype='float')
        tfm_mat[0:3,0:3]=Rot_mat
        tfm_mat[0:3,3]=trans_vec
        tfm_mat[3,3]=1
        # print tfm_mat
        # finding new Q w.r.to transformation matrix 'tfm_mat'
        Q=[]
        for loop in range(len(p_cl2)):
            tmp=np.dot(tfm_mat,[p_cl2[loop,0],p_cl2[loop,1],p_cl2[loop,2],1])
            p_cl2_tmp=tmp[0:3]/float(tmp[3])
            Q.append(p_cl2_tmp)
        p_cl2=np.asarray(Q)
        
            
    # Final Q (i.e) transformed point cloud 2 is given by
    Q_trans=p_cl2
    return Q_trans
#########################################
# ICP algorithm ends here
#########################################
 
#########################################
# Finding correspondence starts here
#########################################

def Corres(p_1,p_2,threshold):
    
    corres_p=[]
    corres_q=[]
    #p_cl2_dummy
    p_cl2_dummy=p_2
    #idx=None
    dummy_mat=np.zeros((p_1.shape[0],6))
    count=0
    idx_list=[]
    for loop1 in range(len(p_1)):
        
        diff_sq=(np.subtract(p_1[loop1,:],p_cl2_dummy[:,:])**2)
        
        euc=np.sqrt(diff_sq[:,0]+diff_sq[:,1]+diff_sq[:,2])
        
        idx=np.argmin(euc)
        min_val=np.min(euc)
        #print idx
        if idx in idx_list:
            continue
        if threshold>min_val:
            # List cannot be used in python since it uses late binding
            #corres_p.append(p_1[loop1,:])
            #corres_q.append(p_2[idx,:])
            dummy_mat[count,:]=(p_1[loop1,0],p_1[loop1,1],p_1[loop1,2],p_2[idx,0],p_2[idx,1],p_2[idx,2])
            count+=1
            idx_list.append(idx)
        else:
            continue
    idx_list=np.asarray(idx_list)
    for loop in range(len(dummy_mat)):
        if dummy_mat[loop,0]!=0 or dummy_mat[loop,1]!=0 or dummy_mat[loop,2]!=0 or dummy_mat[loop,4]!=0 or dummy_mat[loop,5]!=0 or dummy_mat[loop,3]!=0:
            corres_p.append(dummy_mat[loop,0:3])
            corres_q.append(dummy_mat[loop,3:6])
            
    # print "after finding correspondence"
    return np.asarray(corres_p),np.asarray(corres_q)
    
#########################################
# Finding correspondence ends here
######################################### 
