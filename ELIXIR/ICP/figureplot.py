#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdbreader
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_icp2(pointA,pointB,filename):

    plt.figure()
    ax2 = plt.subplot(111, projection='3d')  # create a 3D figure

    ax2.scatter(pointA[:,0],pointA[:,1],pointA[:,2], c='r',label='O104')  # make the points
    ax2.scatter(pointB[:,0],pointB[:,1],pointB[:,2], c='y',label='PBP')

    # ax2.scatter(pointC[:,0],pointC[:,1],pointC[:,2], c='g',label='ICP')

    ax2.set_zlabel('Z')  # coor label
    ax2.set_ylabel('Y')
    ax2.set_xlabel('X')
    ax2.legend()
    plt.savefig(filename+'.png')
    # plt.figure()
    # ax = plt.subplot(111, projection='3d')  # create a 3D figure
    #
    # ax.scatter(pointA[:,0],pointA[:,1],pointA[:,2], c='y',label='O104')  # make the points
    # # ax.scatter(pointB[:,0],pointB[:,1],pointB[:,2], c='r',label='PBP')
    # ax.scatter(pointC[:,0],pointC[:,1],pointC[:,2], c='b',label='ICP')
    #
    # ax.set_zlabel('Z')  # coor label
    # ax.set_ylabel('Y')
    # ax.set_xlabel('X'+' Number of iteations:'+str(pointC[-1,-1]))
    # ax.legend()
    plt.show()
    plt.close()

def plot_icp(pointA,pointB,filename):

    plt.figure()
    ax2 = plt.subplot(111, projection='3d')  # create a 3D figure

    ax2.scatter(pointA[:,0],pointA[:,1],pointA[:,2], c='r',label='O104')  # make the points
    ax2.scatter(pointB[:,0],pointB[:,1],pointB[:,2], c='g',label='Optimized PBP')
    # ax2.scatter(pointC[:,0],pointC[:,1],pointC[:,2], c='g',label='ICP')

    ax2.set_zlabel('Z')  # coor label
    ax2.set_ylabel('Y')
    ax2.set_xlabel('X')
    ax2.legend()
    plt.savefig(filename+'.png')
    # plt.figure()
    # ax = plt.subplot(111, projection='3d')  # create a 3D figure
    #
    # ax.scatter(pointA[:,0],pointA[:,1],pointA[:,2], c='y',label='O104')  # make the points
    # # ax.scatter(pointB[:,0],pointB[:,1],pointB[:,2], c='r',label='PBP')
    # ax.scatter(pointC[:,0],pointC[:,1],pointC[:,2], c='b',label='ICP')
    #
    # ax.set_zlabel('Z')  # coor label
    # ax.set_ylabel('Y')
    # ax.set_xlabel('X'+' Number of iteations:'+str(pointC[-1,-1]))
    # ax.legend()
    plt.show()
    plt.close()

def plot_icp3(pointA,pointB,pointC,filename):

    plt.figure()
    ax2 = plt.subplot(111, projection='3d')  # create a 3D figure

    ax2.scatter(pointA[:,0],pointA[:,1],pointA[:,2], c='r',label='O104')  # make the points
    ax2.scatter(pointB[:,0],pointB[:,1],pointB[:,2], c='g',label='Optimiezd PBP')
    ax2.scatter(pointC[:, 0], pointC[:, 1], pointC[:, 2], c='y', label='PBP')



    ax2.set_zlabel('Z')  # coor label
    ax2.set_ylabel('Y')
    ax2.set_xlabel('X')
    ax2.legend()
    plt.savefig(filename+'_3points.png')
    # plt.figure()
    # ax = plt.subplot(111, projection='3d')  # create a 3D figure
    #
    # ax.scatter(pointA[:,0],pointA[:,1],pointA[:,2], c='y',label='O104')  # make the points
    # # ax.scatter(pointB[:,0],pointB[:,1],pointB[:,2], c='r',label='PBP')
    # ax.scatter(pointC[:,0],pointC[:,1],pointC[:,2], c='b',label='ICP')
    #
    # ax.set_zlabel('Z')  # coor label
    # ax.set_ylabel('Y')
    # ax.set_xlabel('X'+' Number of iteations:'+str(pointC[-1,-1]))
    # ax.legend()
    plt.show()
    plt.close()