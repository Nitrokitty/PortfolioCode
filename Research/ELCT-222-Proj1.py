# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 16:58:10 2015

@author: Rogue
"""

import numpy as np, matplotlib.pyplot as plt

#Question 1
R = 1*10**4
C = 5*10**-7
w = np.logspace(-3, 3, 100)
def Hdb(w):
    return 20*np.log(H(w))
def H(w):
    return abs((-2*R*w*C+1-(R*w*C)**2)**-1)
def p(w):
    return np.rad2deg(-np.arctan(Hdb(w)))

#Problem 1
plt.xscale('log'); 
plt.ylim([-40, 5]); 
plt.ylabel("Hdb(w/wc)"); 
plt.xlabel("w/wc");
plt.title("Cascaded Filter: Frequency Response"); 
plt.plot(w, Hdb(w)); 
plt.savefig("C:\\Users\\Rogue\\Google Drive\\School\\ELCT 222\\project1-1-Hdb.jpg")

plt.figure()
plt.xscale('log'); 
plt.ylim([90, -90]); 
plt.ylabel("Phase Angle(degrees)"); 
plt.xlabel("w/wc");
plt.title("Cascaded Filter: Phase Angle"); 
plt.plot(w, p(w)); 
plt.savefig("C:\\Users\\Rogue\\Google Drive\\School\\ELCT 222\\project1-1-p.jpg")

#problem 2
R = 10000
C1 = 4.496*10**-9
C2 = 2.482*10**-9
w1 = np.logspace(-3, 0, 100)
w2 = np.logspace(0, 3, 100)

def p(w):
    return np.rad2deg(-np.arctan(Hdb(w)))
def H(w):
    return abs((1-w**2-w*np.sqrt(2))**-1)
def p2(w):
    return np.rad2deg(-180-np.arctan(Hdb(w)))

plt.figure()
plt.xscale('log'); 
plt.ylim([-40, 5]); 
plt.ylabel("Hdb(w/wc)"); 
plt.xlabel("w/wc");
plt.title("Butterworth Filter: Frequency Response"); 
plt.plot(w, Hdb(w)); 
plt.savefig("C:\\Users\\Rogue\\Google Drive\\School\\ELCT 222\\project1-2-Hdb.jpg")

plt.figure()
plt.xscale('log'); 
plt.ylim([180, -180]); 
plt.ylabel("Phase Angle(degrees)"); 
plt.xlabel("w/wc");
plt.title("Butterworth Filter: Phase Angle"); 
plt.plot(w, p(w));
plt.savefig("C:\\Users\\Rogue\\Google Drive\\School\\ELCT 222\\project1-2-p.jpg")