import numpy as np
from scipy.ndimage import white_tophat

def staffs(image, radius=2, depth_ang=1, depth_rad=1, threshold=50):
    import numpy as np
    '''def Dx(image):
        return image[1:,:]-image[:-1,:]'''
    def defining(img):
        image=img.copy()
        zero=np.zeros_like(image)
        for y in range(image.shape[0]):
            if image[y].sum()>image.shape[0]*2/3:
                zero[y]=1
        return zero
                

    def houghie(img, radius=2, depth_ang=1, depth_rad=1):
        image=img.copy()
        xs, ys=image.shape
        #final_list=[]
        hough = np.zeros((int(np.sqrt(xs**2+ys**2)),181))
        #print hough.shape
        for yo in range(radius,len(image[0,:])-radius-1):
            for xo in range(radius,len(image[:,0])-radius-1):
                if image[xo,yo]:
                    my_section=image[xo-radius:xo+radius+1,yo-radius:yo+radius+1]
                    section=my_section.copy()
                    section[radius,radius]=False
                    xo_list,yo_list=np.where(section)
                    for i in range(len(yo_list)):
                        x1=xo_list[i]+xo-radius; y1=yo_list[i]+yo-radius
                        theta=np.arctan2(float(yo-y1),float(x1-xo))
                        r=(yo*np.cos(theta)+xo*np.sin(theta))
                        if theta<0:
                            theta+=np.pi
                        p_cord=[r, theta]
                        #final_list.append(p_cord)
                        hough[int(abs(r*depth_rad)), int(np.rad2deg(theta)*depth_ang)] += 1
        return hough


    def lines(image, hough, depth_ang=1, depth_rad=1):
        z=np.zeros_like(image)
        x=[]
        for xo in range(len(hough[:,0])):
            yo=90
            if float(hough[xo, yo])/hough.max()>=.5:
                x.append([hough[xo,yo], xo, yo])
            x.sort()
        #while len(x)%5!=0 or len(x)>50:
            #del(x[0])
        print x
        for item in x:
            if item[1]<z.shape[0]:
                for i in range(z.shape[1]):
                    z[item[1], i]+=1
        return z


    return defining(image)


def seek(image, item):
        return white_tophat(image, footprint=item)

'''def notes(image):
    quarter=np.fromfunction(lambda i,j: (i-3)**2+(j-3)**2<=10, (7,7))
    half=np.array([[False, False,  False,  False,  True,  True,  True,  True,  True],
       [False,  False,  True,  True,  True, False, False, False,  True],
       [False,  True,  True, False, False, False, False, False,  True],
       [ True,  True, False, False, False, False, False,  False,  True],
       [ True, False, False, False, False,  True,  True,  True, False],
       [ True,  True, False,  False,  True,  True,  False, False, False],
       [False,  True,  True,  True,  True, False, False, False, False]])
    return image-seek(seek(image, quarter), half)'''

def notes(array):
    note= np.zeros_like(array)
    def area(labled_array, num_of_lables):
        areas=[]
        for i in range(num_of_lables):
            areas.append((labled_array==i).sum())
        return areas

    def diameter(labled_array, num_of_lables):
        diameter=[]
        im=np.zeros_like(labled_array)
        areas=[]
        sq_area=[]
        '''possibly=[]
        definately=[['label', 'area', 'c_area', 'diameters']]
        probably=[['label', 'area', 'c_area', 'diameters']]'''
        take3=[]
        take2=[]
        for i in range(num_of_lables):
            areas.append((labled_array==i).sum())
        for i in range(num_of_lables):
            x,y=np.where(labled_array==i)
            x.sort; y.sort
            diameter.append([x.max()-x.min(),y.max()-y.min()])
        for i in range(num_of_lables):
            sq_area.append((diameter[i][0])*(diameter[i][1]))
        for i in range(num_of_lables):
            a=sq_area[i]
            '''if diameter[i][0]==diameter[i][1] and int(np.pi)==int(np.pi*((diameter[i][0]/2)**2)):
                definately.append([i, areas[i], np.pi*((diameter[i][0]/2)**2), diameter[i]])
            elif min(diameter[i])/max(diameter[i])>.9 or abs(areas[i]-np.pi*((diameter[i][0]/2)**2))<=1 or abs(areas[i]-np.pi*((diameter[i][1]/2)**2))<=1:
                probably.append([i, areas[i], np.pi*((diameter[i][0]/2)**2), diameter[i]])
            elif min(diameter[i])/max(diameter[i])>.8 or abs(areas[i]-np.pi*((diameter[i][0]/2)**2))<=2 or abs(areas[i]-np.pi*((diameter[i][1]/2)**2))<=2:
                possibly.append([i, areas[i], np.pi*((diameter[i][0]/2)**2), diameter[i]])'''
            '''if abs(diameter[i][0]-diameter[i][1])<=3:
                take2.append([i, diameter[i], areas[i]])'''
            '''if 2*np.sqrt(areas[i]/2*np.pi)>min(diameter[i]) and 2*np.sqrt(areas[i]/np.pi)<max(diameter[i]) and a<200 and a>70:
                take2.append([i, diameter[i], areas[i]])
            if a/((diameter[i][0]/2)*(diameter[i][1]/2)*np.pi )< 1.3 and a/((diameter[i][0]/2)*(diameter[i][1]/2)*np.pi) >.9 and a<200:
                take2.append([i, diameter[i], a])'''
            print min(sq_area), sq_area[i]
            if sq_area[i]<30 and abs(diameter[i][0]-diameter[i][1])<=4:
                take2.append([i, diameter[i], a])
        return take2
    probe=np.array([[0,0,1,0,0],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[0,0,1,0,0]])
    '''L=label(binary_opening(binary_closing(array, probe), probe), np.array([[1,1,1], [1,1,1], [1,1,1]
]))'''
    L=label(binary_dilation(binary_erosion(M, np.fromfunction(lambda i,j: (i-3)**2+(j-3)**2<=10, (7,7)))))
    D=diameter(L[0],L[1])
    for segment in [item[0] for item in D[1:]]:
        note+= L[0]==segment
    lam=np.fromfunction(lambda i,j: (i-3)**2+(j-3)**2<=10, (7,7))
    N=np.zeros_like(note)
    for xo in range(note.shape[1]):
        for yo in range(note.shape[0]):
            if note[yo, xo]:
                N[yo-lam.shape[0]/2:yo+lam.shape[0]/2+1, xo-lam.shape[1]/2:xo+lam.shape[1]/2+1]=lam
    return N

def rests(image):
    quarter_rest=np.array([[False,  True,  True, False, False, False, False, False],
       [False, False,  True,  True, False, False, False, False],
       [False, False, False,  True, False, False, False, False],
       [False, False, False,  True,  True, False, False, False],
       [False, False, False,  True,  True,  True, False, False],
       [False, False, False,  True,  True,  True,  True, False],
       [False, False,  True,  True,  True,  True,  True, False],
       [False, False,  True,  True,  True,  True, False, False],
       [False,  True,  True,  True,  True, False, False, False],
       [False,  True,  True,  True,  True, False, False, False],
       [False, False,  True,  True,  True, False, False, False],
       [False, False, False,  True,  True, False, False, False],
       [False, False, False, False,  True, False, False, False],
       [False,  True,  True,  True,  True,  True, False, False],
       [False,  True,  True,  True,  True,  True,  True, False],
       [ True,  True,  True,  True, False, False,  True,  True],
       [False,  True, False, False, False, False, False, False],
       [False,  True,  True, False, False, False, False, False],
       [False, False,  True,  True, False, False, False, False],
       [False, False, False,  True,  True, False, False, False]])
    return image-seek(image, quarter_rest)

def modifiers(image):
    sharp=np.array([[False,  True,  True, False, False,  True, False],
       [False,  True,  True, False, False,  True, False],
       [False,  True,  True, False, False,  True, False],
       [False,  True,  True, False, False,  True,  True],
       [False,  True,  True,  True,  True,  True,  True],
       [ True,  True,  True,  True,  True,  True,  True],
       [ True,  True,  True,  True,  True,  True, False],
       [ True,  True,  True, False, False,  True, False],
       [False,  True,  True, False, False,  True, False],
       [False,  True,  True, False, False,  True, False],
       [False,  True,  True, False, False,  True,  True],
       [False,  True,  True,  True,  True,  True,  True],
       [ True,  True,  True,  True,  True,  True,  True],
       [ True,  True,  True,  True,  True,  True, False],
       [ True,  True,  True, False, False,  True, False],
       [False,  True,  True, False, False,  True, False],
       [False,  True,  True, False, False,  True, False],
       [False,  True,  True, False, False, False, False]])

    return image-seek(image, sharp)

def clefs(image_nolines):
        import numpy as np
        from scipy.ndimage import white_tophat
        alto=np.array([[False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False],
           [ True,  True,  True,  True, False,  True,  True, False,  True,
             True,  True, False, False,  True,  True,  True, False, False],
           [ True,  True,  True,  True, False,  True,  True,  True,  True,
             True,  True, False, False, False,  True,  True,  True, False],
           [ True,  True,  True,  True, False,  True,  True,  True,  True,
             True,  True,  True, False, False,  True,  True,  True,  True],
           [ True,  True,  True,  True, False,  True,  True,  True,  True,
             True,  True,  True, False, False,  True,  True,  True,  True],
           [ True,  True,  True,  True, False,  True,  True, False,  True,
             True,  True, False, False, False,  True,  True,  True,  True],
           [ True,  True,  True,  True, False,  True,  True, False, False,
            False, False, False, False, False, False,  True,  True,  True],
           [False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False],
           [ True,  True,  True,  True, False,  True,  True, False, False,
            False, False, False, False, False,  True,  True,  True,  True],
           [ True,  True,  True,  True, False,  True,  True, False, False,
             True, False, False, False, False,  True,  True,  True,  True],
           [ True,  True,  True,  True, False,  True,  True, False,  True,
             True, False, False, False, False,  True,  True,  True, False],
           [ True,  True,  True,  True, False,  True,  True, False,  True,
             True,  True,  True,  True,  True,  True,  True, False, False],
           [ True,  True,  True,  True, False,  True,  True, False,  True,
             True, False, False,  True,  True,  True, False, False, False],
           [ True,  True,  True,  True, False,  True,  True,  True,  True,
             True, False, False, False, False, False, False, False, False],
           [False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False],
           [ True,  True,  True,  True, False,  True,  True,  True,  True,
             True, False, False,  True,  True,  True, False, False, False],
           [ True,  True,  True,  True, False,  True,  True, False,  True,
             True,  True,  True,  True,  True,  True,  True, False, False],
           [ True,  True,  True,  True, False,  True,  True, False,  True,
             True, False, False, False, False,  True,  True,  True, False],
           [ True,  True,  True,  True, False,  True,  True, False,  True,
             True, False, False, False, False,  True,  True,  True,  True],
           [ True,  True,  True,  True, False,  True,  True, False, False,
            False, False, False, False, False,  True,  True,  True,  True],
           [False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False],
           [ True,  True,  True,  True, False,  True,  True, False, False,
            False, False, False, False, False, False,  True,  True,  True],
           [ True,  True,  True,  True, False,  True,  True, False,  True,
             True,  True, False, False, False,  True,  True,  True,  True],
           [ True,  True,  True,  True, False,  True,  True,  True,  True,
             True,  True,  True, False, False,  True,  True,  True,  True],
           [ True,  True,  True,  True, False,  True,  True,  True,  True,
             True,  True,  True, False, False,  True,  True,  True,  True],
           [ True,  True,  True,  True, False,  True,  True,  True,  True,
             True,  True, False, False, False,  True,  True,  True, False],
           [ True,  True,  True,  True, False,  True,  True, False,  True,
             True, False, False, False,  True,  True,  True, False, False],
           [False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False]])
        trebble=np.array([[False, False, False, False, False, False, False, False, False,
            False, False, False,  True,  True, False, False, False, False,
            False],
           [False, False, False, False, False, False, False, False, False,
            False, False,  True,  True,  True,  True, False, False, False,
            False],
           [False, False, False, False, False, False, False, False, False,
            False,  True,  True,  True,  True,  True, False, False, False,
            False],
           [False, False, False, False, False, False, False, False, False,
            False,  True,  True,  True,  True,  True,  True, False, False,
            False],
           [False, False, False, False, False, False, False, False, False,
             True,  True,  True, False, False,  True,  True, False, False,
            False],
           [False, False, False, False, False, False, False, False, False,
             True,  True, False, False, False, False,  True, False, False,
            False],
           [False, False, False, False, False, False, False, False,  True,
             True,  True, False, False, False, False,  True, False, False,
            False],
           [False, False, False, False, False, False, False, False,  True,
             True,  True, False, False, False, False,  True, False, False,
            False],
           [False, False, False, False, False, False, False, False,  True,
             True, False, False, False, False,  True,  True, False, False,
            False],
           [False, False, False, False, False, False, False, False,  True,
             True, False, False, False, False,  True,  True, False, False,
            False],
           [False, False, False, False, False, False, False, False,  True,
             True, False, False, False,  True,  True,  True, False, False,
            False],
           [False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False,
            False],
           [False, False, False, False, False, False, False, False,  True,
             True, False,  True,  True,  True,  True,  True, False, False,
            False],
           [False, False, False, False, False, False, False, False, False,
             True,  True,  True,  True,  True,  True, False, False, False,
            False],
           [False, False, False, False, False, False, False, False, False,
             True,  True,  True,  True,  True, False, False, False, False,
            False],
           [False, False, False, False, False, False, False, False,  True,
             True,  True,  True,  True,  True, False, False, False, False,
            False],
           [False, False, False, False, False, False, False,  True,  True,
             True,  True,  True,  True, False, False, False, False, False,
            False],
           [False, False, False, False, False, False,  True,  True,  True,
             True,  True,  True, False, False, False, False, False, False,
            False],
           [False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False,
            False],
           [False, False, False,  True,  True,  True,  True,  True,  True,
            False,  True, False, False, False, False, False, False, False,
            False],
           [False, False, False,  True,  True,  True,  True,  True, False,
            False,  True, False, False, False, False, False, False, False,
            False],
           [False, False,  True,  True,  True,  True,  True, False, False,
            False,  True, False, False, False, False, False, False, False,
            False],
           [False,  True,  True,  True,  True,  True, False, False, False,
            False,  True, False, False, False, False, False, False, False,
            False],
           [False,  True,  True,  True,  True, False, False, False, False,
            False,  True, False, False, False, False, False, False, False,
            False],
           [False,  True,  True,  True, False, False, False, False,  True,
             True,  True,  True,  True,  True,  True, False, False, False,
            False],
           [False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False,
            False],
           [ True,  True,  True, False, False, False, False,  True,  True,
             True,  True,  True,  True,  True,  True,  True,  True,  True,
            False],
           [ True,  True,  True, False, False, False,  True,  True,  True,
             True, False,  True, False, False,  True,  True,  True,  True,
            False],
           [ True,  True, False, False, False, False,  True,  True,  True,
            False, False,  True, False, False, False,  True,  True,  True,
             True],
           [ True,  True, False, False, False, False,  True,  True, False,
            False, False,  True, False, False, False, False,  True,  True,
             True],
           [ True,  True,  True, False, False, False,  True,  True, False,
            False, False,  True,  True, False, False, False,  True,  True,
             True],
           [False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False,
            False],
           [False,  True,  True, False, False, False, False,  True, False,
            False, False, False,  True, False, False, False,  True,  True,
             True],
           [False, False,  True,  True, False, False, False, False,  True,
            False, False, False,  True, False, False, False,  True,  True,
            False],
           [False, False,  True,  True,  True, False, False, False,  True,
             True, False, False,  True, False, False, False,  True,  True,
            False],
           [False, False, False,  True,  True,  True, False, False, False,
            False, False, False,  True, False, False,  True,  True, False,
            False],
           [False, False, False, False, False,  True,  True, False, False,
            False, False, False,  True,  True,  True,  True, False, False,
            False],
           [False, False, False, False, False, False, False,  True,  True,
             True,  True,  True,  True,  True,  True, False, False, False,
            False],
           [False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False,
            False],
           [False, False, False, False, False, False, False, False, False,
            False, False, False, False,  True, False, False, False, False,
            False],
           [False, False, False, False, False, False, False, False, False,
            False, False, False, False,  True, False, False, False, False,
            False],
           [False, False, False, False, False, False, False, False, False,
            False, False, False, False,  True, False, False, False, False,
            False],
           [False, False, False, False, False,  True,  True,  True, False,
            False, False, False, False,  True, False, False, False, False,
            False],
           [False, False, False, False,  True,  True,  True,  True,  True,
            False, False, False, False,  True,  True, False, False, False,
            False],
           [False, False, False, False,  True,  True,  True,  True,  True,
             True, False, False, False,  True,  True, False, False, False,
            False],
           [False, False, False,  True,  True,  True,  True,  True,  True,
             True, False, False, False,  True,  True, False, False, False,
            False],
           [False, False, False, False,  True,  True,  True,  True,  True,
            False, False, False, False,  True, False, False, False, False,
            False],
           [False, False, False, False,  True,  True,  True,  True, False,
            False, False, False,  True,  True, False, False, False, False,
            False],
           [False, False, False, False, False,  True,  True, False, False,
            False, False,  True,  True, False, False, False, False, False,
            False],
           [False, False, False, False, False, False, False,  True,  True,
             True,  True,  True, False, False, False, False, False, False,
            False]])
        bass=np.array([[False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False,
            False, False],
           [False, False, False,  True,  True,  True, False, False, False,
            False,  True,  True,  True, False, False, False, False, False,
            False, False],
           [False, False,  True,  True, False, False, False, False, False,
            False,  True,  True,  True,  True, False, False, False,  True,
             True, False],
           [False, False,  True, False, False, False, False, False, False,
            False, False,  True,  True,  True,  True, False,  True,  True,
             True,  True],
           [False, False,  True,  True,  True,  True,  True, False, False,
            False, False,  True,  True,  True,  True, False, False,  True,
             True,  True],
           [False,  True,  True,  True,  True,  True,  True, False, False,
            False, False,  True,  True,  True,  True,  True, False, False,
            False, False],
           [False,  True,  True,  True,  True,  True,  True,  True, False,
            False, False,  True,  True,  True,  True,  True, False, False,
            False, False],
           [False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False,
            False, False],
           [False, False,  True,  True,  True,  True,  True, False, False,
            False, False,  True,  True,  True,  True,  True, False, False,
            False, False],
           [False, False, False, False,  True,  True, False, False, False,
            False, False,  True,  True,  True,  True,  True, False,  True,
             True,  True],
           [False, False, False, False, False, False, False, False, False,
            False, False,  True,  True,  True,  True, False,  True,  True,
             True,  True],
           [False, False, False, False, False, False, False, False, False,
            False, False,  True,  True,  True,  True, False, False,  True,
             True, False],
           [False, False, False, False, False, False, False, False, False,
            False, False,  True,  True,  True,  True, False, False, False,
            False, False],
           [False, False, False, False, False, False, False, False, False,
            False,  True,  True,  True,  True, False, False, False, False,
            False, False],
           [False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False,
            False, False],
           [False, False, False, False, False, False, False, False, False,
             True,  True,  True,  True, False, False, False, False, False,
            False, False],
           [False, False, False, False, False, False, False, False, False,
             True,  True,  True, False, False, False, False, False, False,
            False, False],
           [False, False, False, False, False, False, False, False,  True,
             True,  True, False, False, False, False, False, False, False,
            False, False],
           [False, False, False, False, False, False, False,  True,  True,
             True, False, False, False, False, False, False, False, False,
            False, False],
           [False, False, False, False, False, False,  True,  True,  True,
            False, False, False, False, False, False, False, False, False,
            False, False],
           [False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False,
            False, False],
           [ True,  True,  True,  True,  True, False, False, False, False,
            False, False, False, False, False, False, False, False, False,
            False, False],
           [False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False,
            False, False]])
        return image_nolines-seek(seek(seek(image_nolines, bass), trebble), alto)

def time_signatures(image_nolines):
        four_four=np.array([[False, False, False, False,  True,  True,  True,  True,  True,
        False, False],
       [False, False, False, False,  True,  True,  True,  True, False,
        False, False],
       [False, False, False, False,  True,  True,  True, False,  True,
        False, False],
       [False, False, False,  True,  True,  True, False,  True,  True,
        False, False],
       [False, False, False,  True,  True, False,  True,  True,  True,
        False, False],
       [False, False,  True,  True, False, False,  True,  True,  True,
        False, False],
       [False, False, False, False, False, False, False, False, False,
        False, False],
       [False,  True,  True, False, False, False,  True,  True,  True,
        False, False],
       [ True,  True,  True,  True,  True,  True,  True,  True,  True,
         True,  True],
       [False, False, False, False, False, False,  True,  True,  True,
        False, False],
       [False, False, False, False, False, False,  True,  True,  True,
        False, False],
       [False, False, False, False, False,  True,  True,  True,  True,
         True, False],
       [False, False, False, False,  True,  True,  True,  True,  True,
         True,  True],
       [False, False, False, False, False, False, False, False, False,
        False, False],
       [False, False, False, False,  True,  True,  True,  True, False,
        False, False],
       [False, False, False, False,  True,  True,  True, False,  True,
        False, False],
       [False, False, False,  True,  True,  True, False,  True,  True,
        False, False],
       [False, False, False,  True,  True, False,  True,  True,  True,
        False, False],
       [False, False,  True,  True, False, False,  True,  True,  True,
        False, False],
       [False, False, False, False, False, False, False, False, False,
        False, False],
       [False,  True,  True, False, False, False,  True,  True,  True,
        False, False],
       [ True,  True,  True,  True,  True,  True,  True,  True,  True,
         True,  True],
       [False, False, False, False, False, False,  True,  True,  True,
        False, False],
       [False, False, False, False, False, False,  True,  True,  True,
        False, False],
       [False, False, False, False, False,  True,  True,  True,  True,
         True, False],
       [False, False, False, False,  True,  True,  True,  True,  True,
         True,  True]])
        return image_nolines-seek(image_nolines, four_four)    

def all(image):
    import numpy as np
    from scipy.ndimage import white_tophat
    if len(image.shape)==3:
        image=image[:,:,0]
    if image.dtype!=bool:
        image=image<200
    S=staffs(image)
    thin=S-binary_erosion(S, np.ones((2,1)))
    image_nolines=image-S
    return notes(image)+modifiers(image)+time_signatures(image_nolines)+clefs(image_nolines)+rests(image)+thin




'''def resize(segment, im, increment):
    length, width=im.shape
    for i in range(2,6):
        A=np.tile(segment, (i,i-1))[:,width/i]
        B=np.tile(segment, (i,i))[:length/i, :width/i]
        if (im-white_tophat(im, footprint=A)).max()!=0.0:
            return i, A
        elif (im-white_tophat(im, footprint=B)).max()!=0.0:
            return i, B
    return 0, C'''

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
