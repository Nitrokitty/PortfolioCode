# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 07:56:51 2015

@author: Rogue
"""
from scipy.ndimage import gaussian_filter as gf
import numpy as np, matplotlib.pyplot as plt, cv2, os

os.chdir("C:\\Users\\Rogue\\Documents\\Python Scripts\\Pictures")

c1 = plt.imread("c1.jpg")
c1b = c1
c1 = cv2.resize(c1[:,:,0], (int(c1.shape[1]*.5), int(c1.shape[0]*.5)))
c1 = gf(c1, 1)
c1 = c1 < 75

os.chdir("C:\\Users\\Rogue\\Documents\\Python Scripts\\Custom Classes")

import Hough, Corner_Detection as CD
h, m, im = CD.c.do_all2(c1, 75)
hough, hm, hc = Hough.do_all(c1)


"""POSTER CALLS"""

pp = plt.imread("pTest.png")
pp = cv2.resize(pp, (int(pp.shape[1]*.5), int(pp.shape[0]*.5)))

f1 = Corner_Detection.c.draw_cv_squares(pp, m1, r = 6)





