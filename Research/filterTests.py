# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 08:05:37 2015

@author: Rogue
"""

#Gaussian Filter Tests

import cv2, os, matplotlib.pyplot as plt, numpy as np
os.chdir("C:\\Users\\Rogue\\Documents\\Python Scripts\\Custom Classes")
import Corner_Detection as CD
os.chdir("C:\\Users\\Rogue\\Documents\\Python Scripts\\Pictures")

c = plt.imread("c1.jpg")
c = cv2.resize(c[:,:,0], (int(c.shape[1]*.5), int(c.shape[0]*.5)))
c1 = np.zeros((c.shape[0]+10, c.shape[1]+10))
c1[5:-5, 5:-5] = c
"""c_list = [cv2.GaussianBlur(c1, (1,1), 0), cv2.GaussianBlur(c1, (3,3), 0), cv2.GaussianBlur(c1, (5,5), 0), 
          cv2.GaussianBlur(c1, (7,7), 0), cv2.GaussianBlur(c1, (9,9), 0), cv2.GaussianBlur(c1, (11,11), 0),
        cv2.GaussianBlur(c1, (13,13), 0), cv2.GaussianBlur(c1, (15,15), 0), cv2.GaussianBlur(c1, (31,31), 0)]

c_list = [cv2.GaussianBlur(c1, (31,31), 0), cv2.GaussianBlur(c1, (35,35), 0), cv2.GaussianBlur(c1, (41,41), 0), 
          cv2.GaussianBlur(c1, (47,47), 0), cv2.GaussianBlur(c1, (51,51), 0), cv2.GaussianBlur(c1, (55,55), 0)]

c_list = [cv2.GaussianBlur(c1, (55,55), 0), cv2.GaussianBlur(c1, (61,61), 0), cv2.GaussianBlur(c1, (67,67), 0), 
          cv2.GaussianBlur(c1, (73,73), 0), cv2.GaussianBlur(c1, (79,79), 0), cv2.GaussianBlur(c1, (83,83), 0)]
          
c_list = [cv2.GaussianBlur(c1, (5,5), 1), cv2.GaussianBlur(c1, (5,5), 3), cv2.GaussianBlur(c1, (5,5), 5), 
          cv2.GaussianBlur(c1, (5,5), 7), cv2.GaussianBlur(c1, (5,5), 10), cv2.GaussianBlur(c1, (5,5), 15),
            cv2.GaussianBlur(c1, (5,5), 20), cv2.GaussianBlur(c1, (5,5), 30), cv2.GaussianBlur(c1, (5,5), 40)]

c_list = [cv2.GaussianBlur(c1, (5,5), 1), cv2.GaussianBlur(c1, (11,11), 1), cv2.GaussianBlur(c1, (15,15), 1), 
          cv2.GaussianBlur(c1, (21,21), 1), cv2.GaussianBlur(c1, (25,25), 1), cv2.GaussianBlur(c1, (29,29), 1)]
    
c_list = [cv2.GaussianBlur(c1, (1,1), 1), cv2.GaussianBlur(c1, (3,3), 1), cv2.GaussianBlur(c1, (5,5), 1)]"""

c_list = [cv2.GaussianBlur(c1, (1,1), 2), cv2.GaussianBlur(c1, (3,3), 2), cv2.GaussianBlur(c1, (5,5), 2)]
          
c_Mor = []
for item in c_list:
    c_Mor.append(CD.c.Moravec(item))
    
c_Max = []
for item in c_Mor:
    c_Max.append(CD.c.maxie(item))
    
for item in c_Max:
    item.sort()
    plt.imshow(CD.c.draw_cv_squares(c1, item[-20:], 10)); plt.show()