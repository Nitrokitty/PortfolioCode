import numpy as np

class Point:
        def __init__(self):
                self.x = x;
                self.y = y;
                self.z = z;
                self.coordinates = [x, y, z];

        def get_x(self):
                return self.x
        def get_y(self):
                return self.y
        def get_z(self):
                if(self.z == None):
                        print "This point is only in 2D"
                        return;
                return z;
        
        def set_x(self, x1):
                self.x = x1;
                self.set_coordinates([x1, self.y, self.z])
        def set_y(self, y1):
                self.y = y1;
                self.set_coordinates([self.x, y1, self.z])
        def set_z(self, z1):
                self.z = z1;
                self.set_coordinates([self.x, self.y, z1])

        def get_coordinates(self):
                return self.coordinates;

        def set_point(self, x, y, z):
                self.set_x(x)
                self.set_y(y)
                self.set_z(z)
        
        def set_coordinates(self, c):
                self.coordinates = c;

        def get_array(self):
                return np.array([[self.x], [self.y], [self.z]]);


        
        

class Projection():
        def __init__(self):
                self.x_shift = None;
                self.y_shift = None;
                self.proj = None;

        def set_point(self, x, y):
                self.p.set_point(x, y, 0);
                    
        def check_point(self, p = None):
            if( p == None ):
                    p = self.p.get_array();
            if(p.shape[0] != 3 | p.shape[1] != 1):
                print "Invalid point dimesntions";
                return False;
            return True;

        def get_point(self):
                return self.p.get_array();

        def mirror(self, sigma1, sigma2):
            mirr = np.array([[-sigma1, -sigma1, sigma1],  [-sigma2, -sigma2, sigma2], [0, 0, 1]]);
            #print mirr;
            #print self.p.get_array();
            return mirr.dot(self.p.get_array())

        def rotation(self, theta, t_type = 'radians'):
                if(t_type == 'degrees' or t_type == 'd'):
                        theta = (theta*np.pi/180.)
                elif(t_type != 'radians' or t_type != 'r'):
                        print "Angle type not recognized. Use \"degrees\" or \"radians\"."
                        return
                rotate = np.array([[np.cos(theta), np.sin(theta), 0], [-np.sin(theta), np.cos(theta), 0], [0, 0, 1]]);
                return rotate.dot(self.p.get_array());
        
        def shear(self, k, axis = 'x'):
                if(axis == 'x'):
                        sh = np.array([[1, k, 0], [0, 1, 0], [0, 0, 1]]);
                elif(axis == 'y'):
                        sh = np.array([[1, 0, 0], [k, 1, 0], [0, 0, 1]]);
                else:
                        print "Axis Invalid. Use \"x\" or \"y\"";
                        return;
                return sh.dot(self.p.get_array())
        
        def shift(self, x_shift, y_shift):
            displacement = np.array([[1, 0, x_shift], [0, 1, y_shift], [0, 0, 1]]);
            return displacement.dot(self.p.get_array());

        def euclidean_transform(self, theta, tx, ty, t_type = 'radians'):
                if(t_type == 'degrees' or t_type == 'd'):
                        theta = (theta*np.pi/180.)
                elif(t_type != 'radians' or t_type != 'r'):
                        print "Angle type not recognized. Use \"degrees\" or \"radians\"."
                        return
                et = np.array([[np.cos(theta), np.sin(theta), tx], [-np.sin(theta), np.cos(theta), ty], [0, 0, 1]]);
                return et.dot(self.p.get_array())
        
        def translation(self, delta_x, delta_y):
                trans = np.array([[1, 0, 0], [0, 1, 0], [delta_x, delta_y, 1]]);
                return trans.dot(self.p.get_array())
                
        def projective_transform(self, p1, p2, p3, p1d, p2d, p3d):
                det = p1[0]*(p2[1] - p3[1]) - p2[0]*(p1[1] - p3[1]) - p3[0]*(p1[1] - p2[1])
                if(det == 0):
                        print "There is no projective transform for the indicated points"
                        return None;
                mat11 = p1d[0] * (p2[1] - p3[1])
                mat12 = p1d[1] * (p3[0] - p2[0])
                mat13 = p2[0] * p3[1] - p3[0]*p2[1]
                mat21 = p2d[0] * (p3[1] - p1[1])
                mat22 = p2d[1] * (p1[0] - p3[0])
                mat23 = p3[0]*p1[1] - p1[0]*p3[1]
                mat31 = p3d[0] * (p1[1] - p2[1])
                mat32 = p3d[1] * (p2[0] - p1[0])
                mat33 = p1[0]*p2[1] - p2[0]*p1[1]
                proj = np.array([[mat11, mat12, mat13],[mat21, mat22, mat23], [mat31, mat32, mat33]]) / float(det)
                #print proj;
                return proj.dot(self.p.get_array())


        def std_proj(self, p1, p2, p3, p4):
              A = np.mat([[p1[0], p2[0], p3[0]],[p1[1], p2[1], p3[1]], [1., 1., 1.]])
              ell, mu, tau = (A.I).dot( np.mat([[p4[0]], [p4[1]], [1.]]))
              ell = ell.sum(); mu = mu.sum(); tau = tau.sum()
              A = np.mat([[p1[0]*ell, p2[0]*mu, p3[0]*tau],[p1[1]*ell, p2[1]*mu, p3[1]*tau], [ell, mu, tau]])
              return np.mat("0.,0.,1.;0.,-1.,1.;1.,-1.,1.").dot(A.I)

        def new_proj(self, p1, p2, p3, p4, size):
              B = np.mat([[0, 0, size[0]], [0, size[1], size[1]], [1., 1., 1.]])
              ell, mu, tau = (B.I).dot( np.mat([[size[0]], [0], [1]]) )
              ell = ell.sum(); mu = mu.sum(); tau = tau.sum()
              B = np.mat([[0, 0, size[0]*tau], [0, size[1]*mu, size[1]*tau], [ell, mu, tau]])
              
              A = np.mat([[p1[0], p2[0], p3[0]],[p1[1], p2[1], p3[1]], [1., 1., 1.]])
              ell, mu, tau = (A.I).dot( np.mat([[p4[0]], [p4[1]], [1.]]))
              ell = ell.sum(); mu = mu.sum(); tau = tau.sum()
              A = np.mat([[p1[0]*ell, p2[0]*mu, p3[0]*tau],[p1[1]*ell, p2[1]*mu, p3[1]*tau], [ell, mu, tau]])
              return B.dot(A.I)
                
        """p1 --> (0,0); p2 --> (0,1); p3 --> (1, 1); p4 --> (1, 0)"""
        
        def bounding_box(self, image, p1, p2, p3, p4, size):
                p_matrix = self.new_proj(p1, p2, p3, p4, size)
                new_points = lambda x, y: p_matrix.dot(np.mat([[x],[y],[1]], dtype = float))
                y_cord = [0,image.shape[0],image.shape[0], 0]
                x_cord = [0, 0, image.shape[1], image.shape[1]]
                for c in range(4):
                        cord = new_points(y_cord[c], x_cord[c])
                        cord = np.mat(cord/cord[2][0].sum(),dtype = float)
                        y_cord[c] = cord[0][0].sum()
                        x_cord[c] = cord[1][0].sum()
                x_min = int(min(x_cord)); x_max = int(max(x_cord)) +  1; y_min = int(min(y_cord)); y_max = int(max(y_cord)) + 1;
                p_image = np.zeros((y_max - y_min, x_max-x_min))
                for j in range(p_image.shape[0]): #row = y
                        for i in range(p_image.shape[1]): #column = x
                                original = (p_matrix.I).dot(np.mat([[j + y_min],[i + x_min],[1]], dtype = float))
                                original = np.mat(original/original[2][0], dtype = int)
                                y = original[0][0].sum(); x = original[1][0].sum() 
                                if( x < 0 or y < 0 or y >= image.shape[0] or x >= image.shape[1]):
                                        i = i
                                else:
                                        p_image[j][i] = image[y][x]
                return p_image, p_matrix

        def I_proj( self, image, p1, p2, p3, p4, size):
                p_matrix = self.new_proj(p1, p2, p3, p4, size)
                pp = p_matrix.dot(np.mat([[p1[0]],[p1[1]], [1]]))
                x_cord = [p1[0],p2[0],p3[0], p4[0]]
                y_cord = [p1[1],p2[1],p3[1], p4[1]]
                p_image = np.zeros(size)
                for j in range(size[0]): #row = y
                        for i in range(size[1]): #column = x
                                original = (p_matrix.I).dot(np.mat([[j],[i],[1]], dtype = float))
                                original = np.mat(original/original[2][0], dtype = int)
                                x = original[0][0].sum(); y = original[1][0].sum()
                                if( x < 0 or y < 0 or x >= image.shape[0] or y >= image.shape[1]):
                                        i = i
                                else:
                                        p_image[j][i] = image[x][y]        
                return p_image, p_matrix

        def plot_all(self, image, p1, p2, p3, p4, size):
                bb, sample = p.both(test, [822.,68.], [302., 527.], [1582., 1035.], [1866., 284.], [516, 258])
                plt.close('all')
                plt.figure()
                plt.subplot(131); plt.imshow(image);
                plt.subplot(132); plt.imshow(bb);
                plt.subplot(133); plt.imshow(sample);
                plt.show()

        
                                

            
'''
t = np.pi/9;
point = np.array([0, 0, 1]);
sigmas = [2*(36/25.), 2*(-48/25.)]
axis = [2, 0]

problem1 = mirror(point, sigmas[0], sigmas[1])

problem2 = mirror(shift(rotation(shift(point, axis[0], axis[1]), t), -axis[0], axis[1]), sigmas[0], sigmas[1])

problem3 = shift(rotation(shift(mirror(point, sigmas[0], sigmas[1]), axis[0], axis[1]),t), -axis[0], axis[1])
'''
from skimage.data import text
import numpy as np, matplotlib.pyplot as plt, os
from scipy.ndimage import imread
os.chdir("C:\Users\Rogue\Documents\Python Scripts")
test = imread("pTest.png")
test = test[:,:,0]
os.chdir("C:\Users\Rogue\Documents\Python Scripts\Custom Classes")

p = Projection()
'''
#im3, pmat = p.I_proj(image, [8., 139.], [86., 347.], [134., 277.], [37., 65.], [64,120])
#im4, pmat = p.I_proj(image, [79., 67.], [79., 103.], [99., 108.], [99., 67.], [256,256])
#im5, pm = p.bounding_box(image, [8., 139.], [86., 347.], [134., 277.], [37., 65.], [64,120])

                    
x     y       X     Y    P
68    822     0     0    1
527   302     0     1    2
1035  1582    1     1    3
284   1866    1     0    4


bb, bp = p.bounding_box(test, [822.,68.], [302., 527.], [1582., 1035.], [1866., 284.], [4096, 2048]);
sample, sp = p.I_proj(test, [822.,68.], [302., 527.], [1582., 1035.], [1866., 284.], [4096, 2048])
plt.close('all')
plt.figure()
plt.subplot(131); plt.imshow(test);
plt.subplot(132); plt.imshow(bb);
plt.subplot(133); plt.imshow(sample);
plt.show()'''