import numpy as np
import matplotlib.pyplot as plt

def isBall(x, y, h, k, r):
    return (x-h)**2+(y-k)**2 <= r**2

def drawBallNP(image, h, k, r):
	mask = np.array(image, dtype=int)
	result = np.fromfunction(lambda i, j: (i-h)**2+(j-k)**2 <= r**2, (len(image[:,0]), len(image[0, :])))
	return mask+result > 0

def drawHole(image, h, k, r1, r2):
	mask = np.array(image, dtype=int)
	result1 = np.fromfunction(lambda i, j: (i-h)**2+(j-k)**2 <= r1**2, (len(image[:,0]), len(image[0, :])))
	result2 = np.fromfunction(lambda i, j: (i-h)**2+(j-k)**2 <= r2**2, (len(image[:,0]), len(image[0, :])))
	result = result1 - result2
	return mask+result > 0

def draw_line(image, a, b, c, epsilon = 1):
	mask = np.array(image, dtype=int)
	result = np.fromfunction(lambda i, j: abs(a*i+b*j-c) <= epsilon, (len(image[:,0]), len(image[0, :])))
	return mask+result > 0

def drawTangentLine(image, r, theta, ep = .009):
	mask = np.array(image, dtype=int)
	result = np.fromfunction(lambda x, y:  ep >= abs((np.cos(theta)*x+np.sin(theta)*y) - r), (len(image[:,0]), len(image[0, :])))
	return mask+result > 0 
	
def isLine(x, y, m ,b, t):
    return abs(y - (m*x+b)) <=t

def drawBasicLine(image, m, b, epsilon):
	mask = np.array(image, dtype=int)
	result = np.fromfunction(lambda i, j: abs(j - (m*i+b)) <= epsilon, (len(image[:,0]), len(image[0, :])))
	return mask+result > 0 


def plotTrue(image, axis = False):
    if axis:
        plt.axis([0, len(image[0,:])-1, 0, len(image[:, 0])-1])
    plt.imshow(image)
    plt.show()
    if axis:
        plt.axis('off')

def plot(images):
    for i in range(len(images)):
        plt.subplot(1, len(images), i+1)
        plt.imshow(images[i])
    plt.show();
    plt.close('all');

img = np.ones((512,512)) == 0

#drawing Balls
drawBall(img, 450, 80, 20)
drawBall(img, 100, 100, 60)
drawBall(img, 360, 420, 90)
drawBall(img, 100, 300, 40)
drawBall(img, 100, 350, 50)


#drawing Lines
drawBasicLine(img, 1, 5, 3)
for j in range(len(img[:,0])):
        for i in range(len(img[0,:])):
            if abs(370 - j) <= 1:
                img[j,i] = True
for j in range(len(img[:,0])):
        for i in range(len(img[0,:])):
            if abs(25 - i) <= 1:
                img[j,i] = True

img2 = np.zeros((100,100))
img2 = drawHole(img2, 50, 50, 10, 6)
img2 = drawHole(img2, 80, 60, 7, 5)
img2 = drawHole(img2, 20, 20, 12, 10)

#plt.gray(); plot(img)

s1 = np.ones((3,3))
s2 = np.array([[0,1,0],[1,1,1],[0,1,0]])

'''
#Morphology
close = binary_closing(img) #no change
open = binary_opening(img) #no change

erode = binary_erosion(img)
erode1 = binary_erosion(img, s1)
erode2 = binary_erosion(img, s2)

fill = binary_fill_holes(img) #filled in the triangle!!! neat!
fill1 = binary_fill_holes(img, s1) #still filled the triangle
fill2 = binary_fill_holes(img, s2) #same

hitMiss = binary_hit_or_miss(img) #all filled in? all black?!?! oh no pattern was found
hitMiss1 = binary_hit_or_miss(img, s1) #found the 3x3 in almost all of the shapes except a line. it wasnt thick enough
hitMiss2 = binary_hit_or_miss(img, s2) #weird that it didnt find the cross pattern... must have to be exact
hitMiss3 = binary_hit_or_miss(img, np.array([[1,0,0],[1,0,0],[1,0,0]])) #this found all of the right sides of the circles just as i thought!!

prop = binary_propagation(img) #all black again
#tried it with the others, even with erroded images and they all came back black even though it's supposed to "reconstruct" eroded images

#gets rid of most of the lines
black_tophat(img, footprint = s1)
black_tophat(img, footprint = s2) 

distance_transform_bf(img) #gets rid of the lines and blurs the spheres
distance_transform_cdt(img) #this one does the same thing, but faster

grey_dilation(img, footprint = s1) #same as binary
grey_erosion(img, fooprint = s1) #same as binary
grey_opening(img, footprint = s1) #same as binary
grey_closing(img, footprint = s1) #same as binary

morphological_gradient(img, s1) #creates an outline of all of the structures!! neat!
morphological_gradient(img, s2) #even thinner outline

morphological_laplace(img, footprint = s2) #no change

white_tophat(img, footprint = s1) #left the diagnoal line and a few points of the circle
plot(white_tophat(img, footprint = s2)) #left nothing


def drawPolarLine(r, theta, ep):
	def y(x):
		return np.sqrt((xo*np.cos(theta))**2+(yo*np.sin(theta))+2*xo*yp*np.cos(theta)*np.sin(theta) - x**2)
	x = xo - np.tan(theta)*(y(
'''
