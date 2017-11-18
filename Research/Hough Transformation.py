import numpy as np

def houghie(img, radius=2, depth_ang=1, depth_rad=1):
    image=img.copy()
    final_list=[]
    hough = np.zeros((np.sqrt(img.shape[0]**2+img.shape[1]**2)*depth_rad,360*depth_ang))
    for yo in range(radius,len(image[0,:])-radius-2):
        for xo in range(radius,len(image[:,0])-radius-2):
            if image[xo,yo]:
                my_section=image[xo-radius:xo+radius+1,yo-radius:yo+radius+1]
                section=my_section.copy()
                section[radius,radius]=False
                xo_list, yo_list=np.where(section)
                for i in range(len(yo_list)):
                    x1=xo_list[i]+xo-radius; y1=yo_list[i]+yo-radius
                    theta=np.arctan2(float(yo-y1),float(x1-xo))
                    r=(yo*np.cos(theta)+xo*np.sin(theta))
                    if theta<0:
                        theta+=np.pi
                    p_cord=[r, theta]
                    final_list.append(p_cord)
                    hough[int(abs(r*depth_rad)), int(np.rad2deg(theta)*depth_ang)] += 1
    return hough
