# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 17:26:53 2015

@author: Rogue
"""

import numpy as np, os, matplotlib.pyplot as plt, subprocess
import Corner_Detection as CD

savePath = "//acct//talleyad//Documents//Research//CScripts"

def translateArray(array, filename = "outArray.txt"): 
	global savePath;
	s = "";
	height, width = array.shape
	for x in range(height): #height
	    for y in range(width): #width
	            if( x == height and  y == width):
	                s += str(array[x][y])
	            else:
	                s += str(array[x][y])+" "
	currDir = os.getcwd();
	os.chdir(savePath);
	nFile = open(filename, "w+")
	nFile.write(s)
	nFile.close()
	os.chdir(currDir);
	return s;


def translateToPy(filename, width, length):
	a = np.zeros((length, width)).astype(float)
	currDir = os.getcwd()
	os.chdir(savePath);
	newArray = open(filename, "r");
	for j in range(length):
	    s = newArray.readline()
	    for i in range(width):
	        num = s[0: s.find(" ")]
	        a[j][i] = float(num)
	        s = s[s.find(" ")+1:]
	newArray.close()
	os.chdir(currDir);
	return a
	
	
def collect_timings_p( pic, runs):
	lst = []
	for i in range(runs):
	    lst.append(CD.c.Moravec(pic)[1])
	return lst

def collect_timings_c( img, width, height, radius, runs, filename = "timingLog.txt", exe = "./Moravec.out"):
	currDir = os.getcwd();
	os.chdir(savePath);
	subprocess.call(["rm", filename])
	for i in range(runs):
		run_c(img, width, height, radius, exe)
	lst = [];
	cFile = open(filename, "r");
	s = cFile.readline()
	while(s != "" ):
	    lst.append(float(s))
	    s = cFile.readline()
	cFile.close()
	os.chdir(currDir);
	return lst;
	
def collect_timings_all( pPic, runs, imgOut = "oArray.txt", cFilename = "time.txt", exe = "./Moravec.out", radius = 1):
	lst = [["Python", "C++", "%Improvement"]];
	l, w = pPic.shape
	translateArray(pPic, imgOut)
	print("Collecting Python Timings")
	pLst = collect_timings_p(pPic, runs)
	print("Collecing C Timings")
	cLst = collect_timings_c(imgOut, w, l, radius, runs, cFilename, exe)
	for i in range(len(pLst)):
	    lst.append([pLst[i], cLst[i], str(pLst[i]*100/cLst[i]) + "%"])
	print("Cleaning Up")
	subprocess.call(["rm", imgOut])
	return lst

def run_c(img, width, height, radius, exe = "./Moravec.out"):
	subprocess.call([exe, img, str(width), str(height), str(radius)])

def changePath(path):
	global savePath
	savePath = path;

def getPath():
	global savePath;
	return savePath;
