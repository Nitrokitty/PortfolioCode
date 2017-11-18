# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 10:38:08 2015

@author: Rogue
"""
import numpy as np, matplotlib.pyplot as plt, os, cv2

os.chdir("C:\\Users\\Rogue\\Documents\\Python Scripts\\Custom Classes")
import Corner_Detection as CD

os.chdir("C:\\Users\\Rogue\\Documents\\Python Scripts\\Pictures")
c1 = plt.imread("c1.jpg")
c1 = cv2.resize(c1[:,:,0], (int(c1.shape[1]*.5), int(c1.shape[0]*.5)))
c1 = c1<75
c3 = plt.imread("c3.jpg")
c3 = cv2.resize(c3[:,:,0], (int(c3.shape[1]*.4), int(c3.shape[0]*.4)))
c3 = c3<175
c4 = plt.imread("c4.jpg")
c4 = cv2.resize(c4[:,:,0], (int(c4.shape[1]*.25), int(c4.shape[0]*.25)))
c4 = c4 < 200
c5 = plt.imread("c5.jpg")
c5 = cv2.resize(c5[:,:,0], (int(c5.shape[1]*.6), int(c5.shape[0]*.6)))
c5 = c5 < 140
c7 = plt.imread("c7.jpg")
c7 = cv2.resize(c7[:,:,0], (int(c7.shape[1]*.2), int(c7.shape[0]*.2)))
c7 = c7 < 90
os.chdir("C:\\Users\\Rogue\\Documents\\Python Scripts")

images= [c1, c3, c4, c5, c7]
ks = [0.4, 0.75, 1.25, 2.13]

os.chdir("C:\\Users\\Rogue\\Documents\\Python Scripts\\Custom Classes")
reload(CD)
os.chdir("C:\\Users\\Rogue\\Documents\\Python Scripts")


def do_all(image, k1):
    hh = CD.c.Harris3(image, k = k1)
    mm = CD.c.maxie(hh)
    im = plot(image, mm)
    return im 

def plot(image, lis):
    im = image.copy().astype(int)
    lis.sort()
    m = im.max()
    for item in lis:
        im[item[1], item[2]] = m*10
    return im
    
j = 2
for im in images:
    plt.figure(1)
    plt.subplot(1,2,1); plt.imshow(im);
    i = 1
    for k in ks:
        ax = plt.subplot(1,2,2); 
        ax.set_title("k = " + str(k))
        plt.imshow(do_all(im, k))
        #plt.savefig("C:\\Users\\Rogue\\Documents\\Python Scripts\\Pictures\\Fin\\fin" + str(j) + str(i)+".jpg", orientation = 'landscape')
        plt.show()
        i+=1
    break
    j+=1
    
        
    
