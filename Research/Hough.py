import numpy as np


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

def conversion(lst, units = "degrees"):
    nlst = []
    for item in lst:
        r = item[1]
        theta = item[2]
        if(units == "degrees" or units == "d"):
            theta = np.deg2rad(theta)
        '''if theta >= 3*np.pi/2:
            theta -= 3*np.pi/2
        elif theta >= np.pi:
            theta -= np.pi
        elif theta >= np.pi/2:
            theta -= np.pi/2
        print theta'''
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        nlst.append((item[0], y, x))
    return nlst

###Hough Transformation Un-Edited###
'''def h_trans(img):
    image=img.copy()
    #final_list=[]
    hough = np.zeros((363,360))
    for yo in range(2,253):
        for xo in range(2,253):
            if image[yo,xo]:
                section=image[yo-2:yo+2,xo-2:xo+2]
                section[2,2]=False
                yo_list,xo_list=np.where(section)
                for i in range(len(xo_list)):
                    y1=yo_list[i]; x1=xo_list[i]
                    theta=np.arctan((x1-xo)/(yo-y1))
                    if theta<0:
                        theta += np.pi
                    r=xo*np.cos(theta)+yo*np.sin(theta)
                    #p_cord=[r, theta]
                    #final_list.append(p_cord)
                    hough[int(r), int(np.rad2deg(theta))] += 1
    return hough'''



###Hough Transform Edited###
def houghie(img, radius=2, depth_ang=1, depth_rad=1):
    image=img.copy()
    final_list=[]
    hough = np.zeros((np.sqrt(img.shape[0]**2+img.shape[1]**2)*depth_rad,360*depth_ang))
    for yo in range(radius,len(image[0,:])-radius-2):
        for xo in range(radius,len(image[:,0])-radius-2):
            if image[xo,yo]:
                #print (yo,xo)
                my_section=image[xo-radius:xo+radius+1,yo-radius:yo+radius+1]
                section=my_section.copy()
                section[radius,radius]=False
                #print section
                xo_list, yo_list=np.where(section)
                #print yo_list
                #print xo_list
                for i in range(len(yo_list)):
                    x1=xo_list[i]+xo-radius; y1=yo_list[i]+yo-radius
                    #print xo, x1, yo, y1
                    theta=np.arctan2(float(yo-y1),float(x1-xo))
                    r=(yo*np.cos(theta)+xo*np.sin(theta))
                    if theta<0:
                        theta+=np.pi
                    p_cord=[r, theta]
                    #print p_cord
                    final_list.append(p_cord)
                    hough[int(abs(r*depth_rad)), int(np.rad2deg(theta)*depth_ang)] += 1
    return hough

def houghie_alt(img, radius=2, depth_ang=1, depth_rad=1):
    image=img.copy()
    final_list=[]
    hough = np.zeros((np.sqrt(img.shape[0]**2+img.shape[1]**2)*depth_rad,360*depth_ang))
    for yo in range(radius,len(image[0,:])-radius-2):
        for xo in range(radius,len(image[:,0])-radius-2):
            if image[xo,yo]:
                #print (yo,xo)
                my_section=image[xo-radius:xo+radius+1,yo-radius:yo+radius+1]
                section=my_section.copy()
                section[radius,radius]=False
                #print section
                yo_list, xo_list=np.where(section)
                #print yo_list
                #print xo_list
                for i in range(len(yo_list)):
                    x1=xo_list[i]+xo-radius; y1=yo_list[i]+yo-radius
                    #print xo, x1, yo, y1
                    theta=np.arctan2(float(yo-y1), float(x1-xo))
                    r=(xo*np.cos(theta)+yo*np.sin(theta))
                    if theta<0:
                        theta+=np.pi
                    p_cord=[r, theta]
                    #print p_cord
                    final_list.append(p_cord)
                    hough[int(abs(r*depth_rad)), int(np.rad2deg(theta)*depth_ang)] += 1
    return hough

def houghie2(img, r = 2, d_ang = 1, d_rad = 1):
    image = img.copy()
    final_list = []
    hough = np.zeros((np.sqrt(img.shape[0]**2+img.shape[1]**2)*depth_rad,360*depth_ang))
    final_list, hough = houghie_helper(0, 0, r, final_list, image, hough)
    return hough
    
def houghie_helper( yo, xo, radius, lst, image, hough):
    my_section=image[xo-radius:xo+radius+1,yo-radius:yo+radius+1]
    section=my_section.copy()
    section[radius,radius]=False
    xo_list, yo_list = np.where(section)
    lst, hough = calculations(0, yo_list, xo_list, yo, xo, r, lst, hough)
    if(yo+1 == image.shape[1] and xo+1 == image.shape[0]):
        return lst, hough
    elif(yo+1 == image.shape[1]):
        lst, hough = houghie_helper(0, xo+1, r, lst, image, hough)
    else:
        lst, hough = houghie_helper(yo+1, xo, r, lst, image, hough)
    return lst, hough
        
def calculations(i, yo_list, xo_list, yo, xo, radius, lst, hough):
    x1=xo_list[i]+xo-radius; y1=yo_list[i]+yo-radius
    theta=np.arctan2(float(yo-y1),float(x1-xo))
    r=(yo*np.cos(theta)+xo*np.sin(theta))
    if theta<0:
        theta+=np.pi
    p_cord=[r, theta]
    final_list.append(p_cord)
    hough[int(abs(r*depth_rad)), int(np.rad2deg(theta)*depth_ang)] += 1
    if(i > len(yo_list) -1):
        return lst, hough
    else:
        lst, hough = calculations(i+1, yo_list, xo_list, yo, xo, r, lst, hough)
    return lst, hough

    

def do_all(image):
    h = houghie(image)
    m = maxie(h)
    c = count(m)
    lst = conversion(m)
    return h, m, c, lst
    
def count(lst, values = False):
    dic = {}
    for item in lst:
        if dic.has_key(item[2]):
            if(values):            
                dic[item[2]] += item[0]
            else:
                dic[item[2]] += 1
        else:
            if(values): 
                dic[item[2]] = item[0]
            else:
                dic[item[2]] = 1
    return dic
    
###Hessian###
'''def  hess(image):
    hough=image.copy()
    def Dx(image):
        return image[1:,:]-image[:-1,:]
    def Dy(image):
        return image[:,1:]-image[:,:-1]
    def Hxx(image):
        return Dx(Dx(image))
    def Hyy(image):
        return Dy(Dy(image))
    def Hxy(image):
        return Dy(Dx(image))
    def Hyx(image):
        return Dx(Dy(image))
    XX=Hxx(hough)[:,:-2]
    X, Y=hough.shape
    Hessian=XX*Hyy(hough)[:-2,:]-(Hxy(hough)[:-1,:-1]*Hyx(hough)[:-1,:-1])
    H_max=np.argwhere(Hessian>0)
    X_max=np.argwhere(XX<0)
    #print X_max
    local_maximums=np.zeros((X,Y))
    for i in range(len(X_max)):
        X_max[i,0]=X_max[i,0]+1
        if X_max[i] in H_max:
            local_maximums[X_max[i,0],X_max[i,1]]+= hough[X_max[i,0],X_max[i,1]]
            print local_maximums.shape
    #print H_max.shape, X_max.shape
    print local_maximums.shape
    return local_maximums'''


###
'''def local_max(image):
    def Dx(image):
        return image[1:,:]-image[:-1,:]
    def Dy(image):
        return image[:,1:]-image[:,:-1]
    X, Y=image.shape
    dX=Dx(image)
    dY=Dy(image)
    #print dX.shape
    #print dY.shape
    l_max=np.zeros(image.shape)
    #print dX[100:110,100:110]
    for y in range(2, Y-2):
        for x in range(2, X-2):
            sec_x=dX[x-1:x+2,y-2:y+1]
            sec_y=dY[x-2:x+1,y-1:y+2]
            #print sec_x.shape, sec_y.shape
            xo=1;yo=1
            if np.sign(sec_x[xo-1,yo-1])!=np.sign(sec_x[xo+1,yo+1]):
                l_max[x,y]+=1
                if np.sign(sec_y[xo-1,yo-1])!=np.sign(sec_y[xo+1,yo+1]):
                    l_max[x,y]+=1
            if np.sign(sec_x[xo-1,yo])!=np.sign(sec_x[xo+1,yo]):
                l_max[x,y]+=1
                if np.sign(sec_y[xo-1,yo])!=np.sign(sec_y[xo+1,yo]):
                    l_max[x,y]+=1
            if np.sign(sec_x[xo,yo-1])!=np.sign(sec_x[xo,yo+1]):
                l_max[x,y]+=1
                if np.sign(sec_y[xo,yo-1])!=np.sign(sec_y[xo,yo+1]):
                    l_max[x,y]+=1
            if np.sign(sec_x[xo-1,yo+1])!=np.sign(sec_x[xo+1,yo-1]):
                l_max[x,y]+=1
                if np.sign(sec_y[xo-1,yo+1])!=np.sign(sec_y[xo+1,yo-1]):
                    l_max[x,y]+=1
    x,y=np.where(l_max>1)
    lst=[]
    for i in range(len(x)):
        lst.append((x[i], y[i], image[x[i],y[i]]))
    return l_max, lst

###Dr's Hoguh###
def houghie(image, radius=5, depth_ang=1, depth_rad=1):
    X, Y = image.shape
    output = np.zeros((int(np.hypot(X,Y)*depth_rad), 360*depth_ang))
    for xo in range(radius,X-radius-1):
        for yo in range(radius,Y-radius-1):
            if image[xo,yo]:
                window = image[max(xo-radius,0):min(xo+radius,X), 
                               max(yo-radius,0):min(yo+radius,Y)]
                x1s, y1s = np.where(window)
                for t in range(len(x1s)):
                    x1 = x1s[t] + xo - radius
                    y1 = y1s[t] + yo - radius
                    if x1!=xo or y1!=yo:
                        theta = np.arctan2(xo-x1,y1-yo)
                        r = (xo*np.cos(theta) + yo*np.sin(theta))*depth_rad
                        print (xo,yo), (x1,y1), (r,theta)
                        rr = int(depth_ang*np.rad2deg(theta+np.pi))
                        if rr<360*depth_ang:
                            output[int(abs(r)),rr]+=1
    return output'''

###Dr's Local Maximum###
def maxie(image, radius=5, threshold=False):
    global np
    X, Y = image.shape
    im = image.copy()
    lst=[]
    output = np.zeros((int(np.hypot(X,Y)),int(np.hypot(X,Y))))
    for xo in range(radius,X-radius-1):
        for yo in range(radius,Y-radius-1):
                value = im[xo,yo]
                window = im[xo-radius:xo+radius, 
                               yo-radius:yo+radius]
                #print window.shape
                #print window[radius, radius], value
                window[radius,radius] = window.min()- 1
                #print window.max()
                #print M
                if value > window.max():
                    output[xo,yo]+=1
                    lst.append((image[xo,yo], xo, yo,))
    if threshold!=False:
        lst.sort()
        return lst[-threshold:]
    else:
        return lst

def maxie2(image, radius=5, threshold=False):
    global np
    X, Y = image.shape
    im = image.copy()
    lst=[]
    output = np.zeros((int(np.hypot(X,Y)),int(np.hypot(X,Y))))
    for xo in range(radius,X-radius-1):
        for yo in range(radius,Y-radius-1):
                value = im[xo,yo]
                window = im[xo-radius:xo+radius, 
                               yo-radius:yo+radius]
                #print window.shape
                #print window[radius, radius], value
                window[radius,radius] = window.min()- 1
                #print window.max()
                #print M
                if value > window.max():
                    output[xo,yo]+=1
                    lst.append((image[xo,yo], xo, yo,))
    lst.sort()
    M = lst[-1][0]
    list_fin = []
    for item in lst:
            if item[0] == M:
                    list_fin.append(item)
    return list_fin



def scorie(maxie):
        scoring=[]
        temp=[]
        copy=[]
        n=0
        d=0
        not_it=[]
        for item in maxie:
                if item[2]==90:
                        scoring.append([item[1], item[0], item[2]])
                        copy.append([item[0], item[1], item[2]])
        scoring.sort()
        for i in range(len(scoring)-1):
                d+=abs(scoring[i+1][0]-scoring[i][0])
                temp.append(abs(scoring[i+1][0]-scoring[i][0]))
        d=d/(len(scoring)-1)
        print d
        count=0
        for i in range(len(temp)):
                print copy
                if copy[i][0]/max(copy)<.5:
                        not_it.append(scoring[i+1])
                print count, temp[i]
                if count%4!=0 or count==0:
                        if d/float(temp[i])<.8:
                                count=-1
                                if temp[i+1]>d:
                                        not_it.append(scoring[i+1])
                                else:
                                        not_it.append(scoring[i])
                        count+=1
                else:
                        count=0
        print not_it
        temp=[]
        for item in scoring:     
                if item not in not_it:
                        temp.append(item)
        return temp
                        
#practice with other hseet music with this and convolve
#search for hough transform to look for circles
    #explain how to do it
