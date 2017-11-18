# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 07:57:50 2015

@author: Rogue
"""

import cv2, os, numpy as np, matplotlib.pyplot as plt
current = os.getcwd()
os.chdir("C:\\Users\\Rogue\\Documents\\Python Scripts\\Custom Classes")
import Corner_Detection as CD
os.chdir(current)

#cap = cv2.VideoCapture(0)      OPEN CAMERA
#cap.release()                  CLOSE CAMERA

def take_pic():
    camera = cv2.VideoCapture(0);
    if(not camera.isOpened()):
        return "Camera could not be opened"
    isCaptured, image = camera.read();
    camera.release()
    if(isCaptured):
        return image
    else:
        return "Unknown Error"

def record_video(filename = None, path = ""):
    camera = cv2.VideoCapture(0);
    if(not camera.isOpened()):
        return "Camera could not be opened"
    if(filename != None):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        if(path == ""):
            path = os.getcwd()+ "\\"
        video_writer = cv2.VideoWriter(path+filename+".avi", fourcc, 20, (680,480))
    while(camera.isOpened()):
        ret, frame = camera.read()
        if ret:
            if(filename != None):
                video_writer.write(frame)
            cv2.imshow("Live Stream", frame)
            w = cv2.waitKey(10)
            if(w == 27): #esc key
                break;
        else:
            break;  
    if(filename != None):
        print "Video was written to "+path+filename+".avi"
        video_writer.release()
    camera.release()
    cv2.destroyAllWindows()
    
def detect_corners(filename = None, path = "", threshold = .5, r = 5):
    harris = CD.c.Harris
    maxie = CD.c.maxie
    #moravec = CD.c.Moravec
    camera = cv2.VideoCapture(0);
    if(not camera.isOpened()):
        return "Camera could not be opened"
    if(filename != None):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        if(path == ""):
            path = os.getcwd()+ "\\"
        video_writer = cv2.VideoWriter(path+filename+".avi", fourcc, 20, (680,480))
    if(camera.isOpened()):
        ret, frame_org = camera.read()
        if ret:
            #frame = frame_orig[:,:,0] < 120
            frame = cv2.resize(frame_org < 120, (int(frame_org.shape[1]*.5), int(frame_org.shape[0]*.5)))
            frame = frame[:,:,0]
            plt.imshow(frame); plt.show()
            response = harris(frame)
            local_max = maxie(response)
            if(filename != None):
                video_writer.write(frame)
            for item in range(len(local_max[-10:])):
                y = item[1]; x = item[2]
                if(y - r > 0 and x - r > 0 and y + r < frame.shape[0] and x + r < frame.shape[1]):
                    cv2.rectangle(frame_orig, (y - r, x - r), (y + r, x + r), 1)
            cv2.imshow("Live Stream", frame)
            """w = cv2.waitKey(10)
            if(w == 27): #esc key
                break;
        else:
            break;  """
    if(filename != None):
        print "Video was written to "+path+filename+".avi"
        video_writer.release()
    camera.release()
    cv2.destroyAllWindows()

def save_pic(filename, image, path = None):
    if(path != None):
        old = os.getcwd()
        os.chdir(path)
        cv2.imwrite(filename +".jpg", image)
        os.chdir(old)
    else:
        cv2.imwrite(filename +".jpg", image)

