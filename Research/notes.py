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
            print abs(diameter[i][0]-diameter[i][1]), sq_area[i]
            if sq_area[i]<35 and abs(diameter[i][0]-diameter[i][1])<=4:
                take2.append([i+1, diameter[i], a])
        print take2
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


'''WT=Wnol-black_tophat(binary_closing(Wnol), footprint=np.fromfunction(lambda i,j: (i-3)**2+(j-3)**2<=10, (8,8)))
WTT=binary_opening(binary_closing(WT, probe), probe)
WB=binary_erosion(W-WWT, np.fromfunction(lambda i,j: (i-3)**2+(j-3)**2<=10, (7,7))'''


