

def all(array):
   
    def staffs(image, radius=2, depth_ang=1, depth_rad=1, threshold=50):
        import numpy as np
        '''def Dx(image):
            return image[1:,:]-image[:-1,:]'''
        def defining(img):
            image=img.copy()
            zero=np.zeros_like(image)
            for y in range(image.shape[0]):
                if image[y].sum()<image.shape[0]*(.5):
                    image[y]=0
            return image
                    

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
            #print x
            for item in x:
                if item[1]<z.shape[0]:
                    z[item[1]]=1
            return z

        def thinning(z):
            zeros=np.zeros_like(z)
            '''L, LN=label(z, np.array([[0,0,0],[1,1,1],[0,0,0]]))
            cordinates=[]
            for i in range(2, LN):
                yo, xo=np.where(L==i)
                if L[yo-1] and L[yo+1]:
                    L[yo-1]=0
                elif L[yo+1] and L[yo-1]==0:
                    L[yo]'''
            cordinates=[]
            T=[]
            yo, xo=np.where(z)
            yo.tolist()
            for i in range(len(yo)):
                if yo[i] not in T:
                    T.append(yo[i])
                    c=1
                    temp=yo[i]
                    while sum(z[yo[i]+c])>0:
                        T.append(yo[i]+c)
                        temp+=yo[i]+c
                        c+=1
                    cordinates.append(temp/c)
            #print cordinates
                
            '''y, x=np.where(L==i)
                y.tolist()
                cordinates.append((y.max()+y.min())/2)'''
            avg_dist=0
            between=[]
            temp=[]
            count=0
            if len(cordinates)%5!=0:
                for i in range(1,len(cordinates)):
                    avg_dist+=(cordinates[i]-cordinates[i-1])
                    between.append(cordinates[i]-cordinates[i-1])
                #print avg_dist
                avg_dist=(avg_dist-max(between))/(len(between)-1)
                #print avg_dist
                #print between
                temp=[]
                #print avg_dist
                for i in range(len(between)):
                    print between[i], count
                    if count%4!=0 or count==0:
                        if avg_dist/float(between[i])<.8:
                            count=-1
                            if between[i+1]>avg_dist:
                                temp.append(cordinates[i+1])
                            else:
                                temp.append(cordinates[i])
                        count+=1
                    else:
                        count=0
            #print temp, cordinates
            for item in cordinates:
                if item not in temp:
                    zeros[item]=1
            return zeros

        return thinning(lines(image, houghie(defining(image))))

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
            take3=[]
            take2=[]
            for i in range(1, num_of_lables+1):
                areas.append((labled_array==i).sum())
            for i in range(1, num_of_lables+1):
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
                #print abs(diameter[i][0]-diameter[i][1]), sq_area[i]
                if sq_area[i]<35 and abs(diameter[i][0]-diameter[i][1])<=4:
                    take2.append([i+1, diameter[i], a])
            #print take2
            return take2
        probe=np.array([[0,0,1,0,0],[0,1,1,1,0],[1,1,1,1,1],[0,1,1,1,0],[0,0,1,0,0]])
        '''L=label(binary_opening(binary_closing(array, probe), probe), np.array([[1,1,1], [1,1,1], [1,1,1]
    ]))'''
        L=label(binary_erosion(array, np.fromfunction(lambda i,j: (i-3)**2+(j-3)**2<=10, (7,7)))
    , np.array([[1,1,1], [1,1,1], [1,1,1]]))
        L1=L[1]
        D=diameter(L[0],L[1])
        print D
        for segment in [item[0] for item in D]:
            note+= L[0]==segment
        lam=np.fromfunction(lambda i,j: (i-2)**2+(j-2)**2<=5, (7,7))
        N=np.zeros_like(note)
        for xo in range(note.shape[1]):
            for yo in range(note.shape[0]):
                if note[yo, xo]:
                    N[yo-lam.shape[0]/2:yo+lam.shape[0]/2+1, xo-lam.shape[1]/2:xo+lam.shape[1]/2+1]=lam
        return N

    def pitches(notes, staffs, clef='not_specified'):
        pitch={}
        cord=[]
        temp=[]
        note_cord={}
        i=1
        trebble={-5:'G3', -4:'A3', -3:'B3',-2:'C4', -1:'D4', 1:'E4', 2:'F4', 3:'G4', 4:'A4', 5:'B4', 6:'C5', 7:'D5', 8:'E5', 9:'F5', 10:'G5', 11:'A5', 12:'B5', 13:'C6', 14:'D6'}
        alto={1:'F3', 2:'G3', 3:'A3', 4:'B3', 5:'C4', 6:'D4', 7:'E4', 8:'F4', 9:'G4'}
        tenor={1:'D3', 2:'E3', 3:'F3', 4:'G3', 5:'A3', 6:'B3', 7:'C4', 8:'D4', 9:'E4'}
        bass={1:'G2', 2:'A2', 3:'B2', 4:'C3', 5:'D3', 6:'E3', 7:'F3', 8:'G3', 9:'A3'}
        spectrum={'G3':-5, 'G#3':-4, 'A3':-3, 'Bb3':-2,'B3':-1,'C4':1, 'C#4':2, 'D4':3, 'Eb4':4, 'E4':5, 'F4':6, 'F#4':9, 'G4':10, 'G#4':11, 'A4':12, 'Bb4':13, 'B4':12, 'C5':13, 'C#5':14,'D5':15,'Eb5':16, 'E5':17, 'F5':18, 'F#5':19, 'G5':20, 'G#5':21, 'A5':22, 'Bb5':23,'B5':24,'C6':25, 'C#6':26, 'D6':27}
        pitches=np.zeros_like(notes).astype(int)
        if clef=='not_specified':
            clef=trebble
        for y in range(staffs.shape[0]):
            if staffs[y, 0]:
                cord.append(y)
                if i%5==0:
                    pitch[y]=9
                else:
                    pitch[y]=(i%5)*2-1
                i+=1
        for i in range(1, len(cord)):
            if (i)%5!=0:
                temp.append((cord[i]+cord[i-1])/2)
                if i%4==0:
                    pitch[(cord[i]+cord[i-1])/2]=8
                else:
                    pitch[(cord[i]+cord[i-1])/2]=(i%4)*2
        cord=cord+temp
        cord.sort()
        #print cord, temp
        average=0  
        '''for i in range(1,8):
            average+=(cord[i]-cord[i-1])
            #print (cord[i]-cord[i-1])
        #print average
        average=average/7
        #print (len(cord)-2)/9
        temp=[]
        for n in range((len(cord))/9):
            for i in range(1,5):
                #print cord[(n*9)]-(average*i), i+9, cord[(n*9)+8]+(average*i), -i
                pitch[cord[(n*9)]-(average*i)]=i+9
                pitch[cord[(n*9)+8]+(average*i)]=-i
                temp.append(cord[n*9]-(average*i))
                temp.append(cord[(n*9)+8]+(average*i))'''
        #print temp
        cord=cord+temp
        cord.sort()
        for item in pitch:
            pitches[item]=1
        #print pitch
        print cord
        L, L_num=label(notes)
        for i in range(1,L_num+1):
            y, x=np.where(L==i)
            avg=0
            for item in y:
                avg+=item
            #print avg
            avg=avg/len(y)
            #print avg
            for item in cord:
                if item==avg and i not in note_cord:
                    note_cord[i]=clef[pitch[item]]
                elif item+1==avg and i not in note_cord:
                    note_cord[i]=clef[pitch[item]]
                elif item-1==avg and i not in note_cord:
                    note_cord[i]=clef[pitch[item]]
            if i in note_cord:
                xo=((x.max()-x.min())/2)+x.min(); yo=((y.max()-y.min())/2)+y.min()
                pitches[yo-3:yo+3, xo-3:xo+3]=spectrum[note_cord[i]]
        return note_cord, pitches
    
    return pitches(notes(array), staffs(array))

