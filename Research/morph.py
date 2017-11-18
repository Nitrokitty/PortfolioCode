import numpy as np
import morph

def erosion(image, probe=np.ones((3,3))):
        length, width = image.shape
        X,Y=probe.shape
        im=np.zeros((length+X, width+Y))
        im[X/2:-X/2, Y/2:-Y/2]=image
        x_probe,y_probe=np.where(probe)
        blank=np.zeros_like(im)
        xy_list=[]
        for i in range(len(x_probe)):
            xy_list.append((x_probe[i], y_probe[i]))
        #print xy_list
        for xo in range(X, length-X):
            for yo in range(Y, width-Y):
                section=im[xo-int(X/2):xo+int(X/2)+1, yo-int(Y/2):yo+int(Y/2)+1]
                #print section.shape, xo, yo, xo-X/2, xo+X/2
                xo_list, yo_list=np.where(section)
                count=0
                if len(xy_list)==len(xo_list):
                    for i in range(len(xo_list)):
                        y1=yo_list[i]; x1=xo_list[i]
                        if (x1,y1) in xy_list:
                            count+=1
                if count==len(xy_list):
                    blank[xo,yo]+=1
        return blank[X/2:-X/2, Y/2:-Y/2]
                            
def dilation(image, probe=np.ones((3,3))):
        length, width = image.shape
        probe=probe>0
        X,Y=probe.shape
        im=np.zeros((length+X, width+Y))
        im[X/2:-X/2, Y/2:-Y/2]=image
        x_probe,y_probe=np.where(probe)
        xy_list=[]
        for i in range(len(x_probe)):
            xy_list.append((x_probe[i], y_probe[i]))
        #print xy_list
        for xo in range(X, length-X):
            for yo in range(Y, width-Y):
                section=image[xo-int(X/2.):xo+int(X/2.)+1, yo-int(Y/2.):yo+int(Y/2.)+1]
                #print section.shape, xo, yo, xo-X/2, xo+X/2
                xo_list, yo_list=np.where(section)
                count=0
                if len(xo_list)<=len(x_probe) and len(xo_list)!=0:
                    for i in range(len(xo_list)):
                        y1=yo_list[i]; x1=xo_list[i]
                        #print x1, y1
                        if (x1,y1) in xy_list:
                            count+=1
                if count>0 and im[xo,yo]==0:
                    im[xo,yo]+=1
        return im[X/2:-X/2, Y/2:-Y/2]

def line_dilation(imag, probe=np.ones((1,7))):
        image=imag-erosion(imag, np.ones((3,1)))
        length, width = image.shape
        probe=probe>0
        X,Y=probe.shape
        im=np.zeros_like(image)
        x_probe,y_probe=np.where(probe)
        xy_list=[]
        for i in range(len(x_probe)):
            xy_list.append((x_probe[i], y_probe[i]))
        #print xy_list
        for xo in range(X, length-X):
            for yo in range(Y, width-Y):
                section=image[xo-int(X/2.):xo+int(X/2.)+1, yo-int(Y/2.):yo+int(Y/2.)+1]
                #print section.shape, xo, yo, xo-X/2, xo+X/2
                xo_list, yo_list=np.where(section)
                count=0
                if len(xo_list)<=len(x_probe) and len(xo_list)!=0:
                    for i in range(len(xo_list)):
                        y1=yo_list[i]; x1=xo_list[i]
                        #print x1, y1
                        if (x1,y1) in xy_list:
                            count+=1
                if count==len(xy_list):
                    im[xo,yo]+=1
        max_list=[]
        for xo in range(length):
                if np.sum(im[xo])>0:
                        max_list.append([np.sum(im[xo]), xo])
        lst=[]
        M=max(max_list)[0]
        for item in max_list:
                if item[0]/M>.50:
                        lst.append(item[1])
        lst.sort()
        while len(lst)%5!=0:
                del(lst[0])
        for xo in range(length):
                if xo not in lst:
                        im[xo]=0
        return im, lst

#def shape_erosion(image, probe=np.ones((

def opening(image, probe=np.array(range(1,10)).reshape((3,3))):
        return morph.dilation(morph.erosion(image, probe), probe)

def closing(image, probe=np.array(range(1,10)).reshape((3,3))):
        return morph.erosion(morph.dilation(image, probe), probe)
