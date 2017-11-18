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
    for i in range(1,8):
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
            temp.append(cord[(n*9)+8]+(average*i))
    #print temp
    cord=cord+temp
    cord.sort()
    '''for item in pitch:
        pitches[item]=1'''
    #print pitch
    #print cord
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
