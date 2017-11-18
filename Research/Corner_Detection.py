import numpy as np, matplotlib.pyplot as plt, os,  time
from scipy.misc import lena
from skimage.transform import rescale
from scipy.ndimage import gaussian_filter



class Corner_Detection():
        def __init__(self):
                self;
                
        def Dx(self, image):
            output = np.zeros_like(image);
            output[:-1,:] = image[1:,:]-image[:-1,:]
            return output

        def Dy(self, image):
            output = np.zeros_like(image)
            output[:,:-1] = image[:,1:]-image[:,:-1]
            return output
            
        def Moravec(self, image, radius = 1):
            start_time = time.time()
            moravec = np.zeros(image.shape)
            for j in range(radius*2, image.shape[0]-radius*2): #rows
                for i in range(radius*2, image.shape[1]-radius*2): #columns
                    piece = image[j-radius:j+radius+1, i-radius:i+radius+1]
                    #print 50*'*'
                    #print piece
                    #print j, i,
                    #print j-radius, j+radius,
                    #print i-radius, i+radius
                    #print 20*'x'
                    for jj in range(-radius, radius+1):
                        for ii in range(-radius, radius+1):
                                #print j, i
                                temp = image[j+jj-radius:jj+j+radius+1, i+ii-radius:ii+i+radius+1]
                                #print str(j+jj-radius) + "\t" + str(j+j+radius+1) + "\t"+ str(i+ii-radius) + "\t" + str(ii+i+radius+1)

                                #print temp.shape
                                if(temp.shape[0]*temp.shape[1] == ((radius*2)+1)**2):
                                        moravec[j,i] += np.sum((piece - temp)**2)
            return moravec, time.time() - start_time

        def Moravec2(self, image, r = 1):
            moravec = np.zeros(image.shape)
            it = np.nditer(image, flags = ['multi_index'])
            window = np.nditer(np.zeros((r+2, r+2)), flags = ['multi_index'])
            while not it.finished:
                pos = it.multi_index
                if(pos[0] >= r and pos[0] + r < moravec.shape[0] and pos[1] >= r and pos[1] + r < moravec.shape[1] ):
                        piece = image[pos[0]-r:pos[0]+r+1, pos[1]-r:pos[1]+r+1]
                        while not window.finished:
                                w = window.multi_index
                                #print w,
                                temp = image[pos[0]+w[0]-(r*2):w[0]+pos[0]+1, pos[1]+w[1]-(r*2):w[1]+pos[1]+1]
                                if(temp.shape[0]*temp.shape[1] == ((r*2)+1)**2):
                                                moravec[pos[0], pos[1]] += np.sum((piece - temp)**2)
                                window.iternext()
                        window.reset()
                        #print ""
                #print it.multi_index
                it.iternext()
            return moravec
            
        def Harris(self, im, radius = 2, lam = .04, threshold = .5):
            #harris = np.zeros(image.shape)
            image = im.copy()
            dxx = self.Dx(self.Dx(image))
            dyy = self.Dy(self.Dy(image))
            dxy = self.Dy(self.Dx(image))
            #dyx = self.Dx(self.Dy(image))
            det =  (dxx * dyy) - (dxy**2)
            tr = dxx + dyy
            response = det - (lam * (tr**2)) #formally response
            #print len((np.where(response > 0))[0])
            #response = response > (response.max() * threshold)
            #print response.max()
            #print np.where(response == response.max())
            #loc_max = self.maxie(response, False, 1)
            corners = (response == response.max()) * response
            corners = self.maxie(corners, False)
            return corners;
            
        def Harris2(self, im, r = 2, k = .04, depth_ang = 1, depth_rad = 1):
            dx, dy = np.gradient(im)
            dxx, dxy = np.gradient(dx)
            dyx, dyy = np.gradient(dy)
            return (dxx*dyy) - (dxy*dyx) - ((k)*(dxx+dyy))

        def Harris3(self, im, r = 2, k = .04, depth_ang = 1, depth_rad = 1):
            har = np.zeros(im.shape)
            for y in range(r, im.shape[0]-r-1):
                for x in range(r, im.shape[1]-r-1):
                    window = im[y-r : y+r-1, x-r:x+r-1]
                    dx, dy = np.gradient(window)
                    dxy = np.gradient(dx)[1]
                    mat = np.array([[np.sum(dx**2), np.sum(dxy**2)],[np.sum(dxy**2), np.sum(dy**2)]])
                    har[y,x] = np.linalg.det(mat) - (k*(mat.trace()**2))
            return har
            
        def harris(self, img, k=0.04, sigma=1.0):   
            dx, dy = np.gradient(img)
            dx2 = gaussian_filter(dx*dx, sigma)
            dy2 = gaussian_filter(dy*dy, sigma)
            dxy = gaussian_filter(dx*dy, sigma)
            return (dx2 * dy2 - dxy**2) - k*(dx2 + dy2)
            
        def harris2(self, img, k=0.04, sigma=1.0):
            dx, dy = np.gradient(img)
            dx = gaussian_filter(dx, sigma)
            dy = gaussian_filter(dy, sigma)
            dx2 = dx*dx
            dy2 = dy*dy
            dxy = dx*dy
            return ((dx2 * dy2) - dxy**2) - k*((dx2 + dy2)**2)
            
        '''                   
        def Harris3(self, im, r = 2, k = .04, depth_ang = 1, depth_rad = 1):
            y, x = im.shape
            har = np.zeros(im.shape)
            self.Har_Help(r, r, r, k, im, har)
            return har
                    
         
        def Har_Help(self, xo, yo, r, k, im, har):
            window = im[yo-r : yo+r-1, xo-r:xo+r-1]
            dx, dy = np.gradient(window)
            dxx = dx**2; dyy = dy**2
            dxy = np.gradient(dx)[1]
            mat = np.array([[np.sum(dx**2), np.sum(dxy**2)],[np.sum(dxy**2), np.sum(dy**2)]])
            #e = np.linalg.eig(mat)[0]
            har[yo,xo] = np.linalg.det(mat) - (k*(mat.trace()**2))
            #End of Image
            if((yo + r == har.shape[0]) and (xo + r == har.shape[1])):
                return
            #End of Row
            elif( xo + r == har.shape[1]):
                return self.Har_Help(r, yo+1, r, k, im, har)
            #Next
            else:
                return self.Har_Help(xo+1, yo, r, k, im, har)

            '''
        def add_border(image):
            y, x = image.shape
            im = np.ones((y*1.25, x*1.25))
            #print x, y
            y1 = y*.125; x1 = x* .125
            y = y1; x = x1
            #print x1, y1
            if(y1%1 != 0):
                y1 = int(y1) + 1
            if(x1%1 != 0):
                x1 = int(x1) + 1
            im[y:-y1, x:-x1] = image
            return im
            
        def local_max(self, image, radius = 1):
            im = np.zeros_like(image)
            for j in range(radius, image.shape[0] - radius): #4
                for i in range(radius, image.shape[1] - radius):
                    selection = image.copy()[j - radius:j+radius+1, i-radius:i+radius+1];
                    lm = selection.max()
                    value = selection[radius, radius]
                    selection[radius, radius] = selection.min()
                    if( value == lm and lm != selection.max()):
                        im[j,i] = im[j,i] + 1;
            return im;
            
        def maxie(self, image, return_lst = True, radius=5, maximum = False):
            global np
            X, Y = image.shape
            im = image.copy()
            lst=[]
            output = np.zeros(image.shape)
            for xo in range(radius,X-radius-1):
                for yo in range(radius,Y-radius-1):
                        value = im[xo,yo]
                        window = (im.copy())[xo-radius:xo+radius, 
                                       yo-radius:yo+radius]
                        window[radius,radius] = window.min()- 1
                        if value > window.max():
                            output[xo,yo]+=1
                            lst.append((image[xo,yo], xo, yo,))
            if(return_lst):
                lst.sort()
                if(maximum):
                        M = lst[-1][0]
                        list_fin = []
                        for item in lst:
                                if item[0] == M:
                                        list_fin.append(item)
                        return list_fin
                else:
                       return lst
            else:
                return output
        
"""
        def squares(self, original, maxima, radius = 3, mag = 5):
            image = original.copy().astype(int)
            yL, xL = original.shape
            for item in maxima:
                y = item[1]; x = item[2]
                if( y - 3 >= 0 and y + 3 < yL and x - 3 >= 0 and x + 3 < xL):
                    for i in range(-radius, radius+1):
                         image[y+i, x-radius] = mag
                         image[y+i, x+radius] = mag
                         image[y-radius, x+i] = mag
                         image[y+radius, x+i] = mag
                else:
                    print("Sqaure radius is too large")
            return image
        def draw_cv_squares(self, original, maxima, r = 3, color = "red"):
            img = original.copy()
            for item in maxima:
                x = item[1]; y = item[2]
                if(y - r > 0 and x - r > 0 and y + r < img.shape[1] and x + r < img.shape[0]):
                        img = cv2.rectangle(img, (y - r, x - r), (y + r, x + r), 1, (0,0,255))
                else:
                    print(y, x)
            return img
            
        def adjust(self, image, thresh, length = 500):        
            im = image.copy()            
            if(len(image.shape) == 3):
                im = im[:,:,0]
            h, w = im.shape
            if(h > w):
                factor = float(length)/float(h)
            else:
                factor = float(length)/float(w)
            print(factor)
            if(factor < 1 and factor > 0):
                im = cv2.resize(im, (int(im.shape[1]*factor), int(im.shape[0]*factor)))
            im = im < thresh
            return im
            
        def do_all(self, image, t):
            im = self.adjust(image, t)
            plt.imshow(im); plt.show()
            h = self.harris(im)
            m = self.maxie(h)
            fin = self.squares(im, m)
            plt.imshow(fin); plt.show()
            return h, m, fin
            
        def do_all2(self, image, t):
            im = self.adjust(image, t)
            plt.imshow(im); plt.show()
            h = self.Harris3(im)
            m = self.maxie(h)
            fin = self.squares(im, m)
            plt.imshow(fin); plt.show()
            return h, m, fin
                    
                
        def maxie2(self, image, return_lst = True, radius=5, maximum = True):
            global np
            X, Y = image.shape
            im = image.copy()
            lst=[]
            output = np.zeros(image.shape)
            for xo in range(radius,X-radius-1):
                for yo in range(radius,Y-radius-1):
                        value = im[xo,yo]
                        window = (im.copy())[xo-radius:xo+radius, 
                                       yo-radius:yo+radius]
                        #window[radius,radius] = window.min()- 1
                        if value == window.max():
                            output[xo,yo]+=1
                            lst.append((image[xo,yo], xo, yo,))
            if(return_lst):
                lst.sort()
                if(maximum):
                        M = lst[-1][0]
                        list_fin = []
                        for item in lst:
                                if item[0] == M:
                                        list_fin.append(item)
                        return list_fin
                else:
                       return lst
            else:
                return output
                """
                
#Instance
c = Corner_Detection();
