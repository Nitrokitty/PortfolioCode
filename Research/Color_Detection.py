# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 13:26:12 2015

@author: Rogue
"""
import numpy as np, os, matplotlib.pyplot as plt, cv2
from scipy.ndimage import binary_closing as bc, gaussian_filter, label


class Color_Detection():
    def __init__(self):
                    self;
    def detect_colors(self, image, prominent = True, top = 10):
        colors = {}
        most = []
        maximum = 0
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                color = image[y,x]
                if colors.has_key(color):
                    colors[color] += 1
                else:
                    colors[color] = 1
                if colors[color] > maximum:
                    maximum = colors[color]
        #print maximum
        if(prominent):
            old_colors = colors
            colors = {}
            for key in old_colors:
                if old_colors[key] >= maximum*.8:
                    colors[key] = old_colors[key]
        return colors
        
    def detect_cluster(self, dictionary, thresh = 1):
        keys = dictionary.viewkeys()
        k = []
        for item in keys:
            k.append(item)
        k.sort()
        ranges = []
        si = k[0]
        ei = k[0]
        r = 0
        for i in range(1, len(k)):
            """print str(k[i]) + "," + str(si)+",",
            print  str(k[i] - si) + ",",
            print str(i)+","+str(k.index(si))+",",
            print thresh*(i - k.index(si))"""
            if not(k[i] - si <= thresh*(i - k.index(si))):
                ranges.append((r, si, ei))
                si = k[i]
                ei = k[i]
                r = 0
            else:
                ei = k[i]
                r += 1
        ranges.append((r, si, ei))
        return ranges
    def largest_area(self, im, num_list):
        ma = 0        
        for i in range(1, num_list+1):
            if(np.sum(im == i) > ma):
                ma = i
        return ma

            
cd = os.getcwd()
os.chdir("C:\\Users\\Rogue\\Documents\\Python Scripts")

sh = plt.imread("pTest.png")
sh = cv2.resize(sh[:,:,0], (int(sh.shape[1]*.5), int(sh.shape[0]*.5)))
sh = gaussian_filter(sh, 10)
sh = (sh*100).astype(int)
CD = Color_Detection()
colors = CD.detect_colors(sh)
cluster = CD.detect_cluster(colors)
cluster.sort()
struct = np.ones((50,50))
sh_fill = bc((sh >= cluster[-1][1]), structure = struct)
plt.imshow(sh_fill); plt.show()
imfin, imnum = label(sh_fill)
c = CD.largest_area(imfin, imnum)
plt.imshow(imfin == c); plt.show()

os.chdir(cd)