import numpy as np
from matplotlib.pyplot import plot, imshow, show
from scipy.ndimage import median_filter

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

def Super_slopes(image,slope=75):
    s1=abs(Dx(image))>slope
    s2=abs(Dy(image))>slope
    s1=s1[:,1:]
    s2=s2[1:,:]
    return s1+s2

def Dtheta(image, theta):
    Dx0=Dx(image)
    Dy0=Dy(image)
    Dx0=Dx0[:,1:]
    Dy0=Dy0[1:,:]
    return np.cos(theta)*Dx0+np.sin(theta)*Dy0

def image_theta(image, theta, integer):
    Im=Dtheta(image, theta)
    imshow(abs(Im)>integer); show()

def many_thetas(m, m10, m25, m50, m75, m90, theta):
    T=Dtheta(m, theta)
    T10=Dtheta(m10, theta)
    T25=Dtheta(m25, theta)
    T50=Dtheta(m50, theta)
    T75=Dtheta(m75, theta)
    T90=Dtheta(m90, theta)
    return T, T10, T25, T50, T75, T90

"""
def m_filter(matrix):
    pi=np.pi
    M=matrix
    M10=median_filter(matrix, 10)
    M25=median_filter(matrix, 25)
    M50=median_filter(matrix, 50)
    M75=median_filter(matrix, 75)
    M90=median_filter(matrix, 90)
    End=np.column_stack((M, M10, M25, M50, M75, M90))
    End=End[1:,6:]
    r=[pi/6, pi/4, pi/3, pi/2, (2*pi)/3, (3*pi)/4, (5*pi)/6]
    for theta in r:
        T=Dtheta(M, theta)
        T10=Dtheta(M10, theta)
        T25=Dtheta(M25, theta)
        T50=Dtheta(M50, theta)
        T75=Dtheta(M75, theta)
        T90=Dtheta(M90, theta)
        print T.shape, T10.shape, T25.shape, T50.shape, T75.shape, T90.shape, End.shape
        temp=0
        temp=np.column_stack((T, T10, T25, T50, T75, T90))
        End=np.row_stack((End, temp))
        print End.shape
    return End
"""       
"""
def theta_filter(matrix):
    T10=Dtheta(
    Col=np.column_stack((matrix, M10, M25, M50, M75, M90))
    print Col.shape
    Col2=np.column_stack((Dtheta(matrix, theta), Dtheta(M10, theta), Dtheta(M25, theta), Dtheta(M50, theta), Dtheta(M75, theta), Dtheta(M90, theta)))
    print Col2.shape
    End=np.row_stack((Col,Col2))
    return End
"""    


##Smoothing##
def smoothing_plot(matrix,smoothing_integer=50, greaterthan_integer=0):
    return imshow(abs(median_filter(matrix, smoothing_integer))>greaterthan_integer)
