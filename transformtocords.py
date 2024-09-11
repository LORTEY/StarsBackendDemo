import math
import os

def getCords(deg): #ra dec dystans
    
    r = deg[2] * math.cos(math.radians(deg[1]))
    z = deg[2] * math.sin(math.radians(deg[1])) # strzałka pozytywna z wskazuje gwiazdę polarną
    
    x = r * math.cos(math.radians(deg[0])) # na x rozpoczyna się kąt ra
    y = r * math.sin(math.radians(deg[0]))
    return [x,y,z]

def getDegrees(planetCords, starCords):
    #zerowanie koordynatów planety dla łatwiejszych obliczeń
    starCords[0] -= planetCords[0]
    starCords[1] -= planetCords[1]
    starCords[2] -= planetCords[2]
    #pobieranie pozostałych wielkości potrzebnych do obliczeń
    r = math.sqrt(starCords[0]**2 + starCords[1]**2)
    Pc = math.sqrt(r**2 + starCords[2]**2)
    Dec = math.degrees(math.asin(starCords[2] / Pc))
    
    #zależnie od ćwiartki układu współrzeędnych wyliczanie kąta RA na niebie
    if starCords[0]>0 and starCords[1]<0:
        RA = 360 + math.degrees(math.asin(starCords[1] / r))
    elif starCords[0]<0 and starCords[1]<0:
        RA = 180 - math.degrees(math.asin(starCords[1] / r))
    elif starCords[0]<0 and starCords[1]>0:
        RA = 180 - math.degrees(math.asin(starCords[1] / r))
    else:
        RA = math.degrees(math.asin(starCords[1] / r))
        
    return [RA, Dec, Pc]

def dataClear(path):
    path = os.path.join(os.path.dirname(__file__),path)
    f = open(path, "r")
    all = f.read()
    f.close()
    cleared = []
    for entry in all.split("\n"):
        if len(entry) > 0:
            cleared.append(entry.split(","))
    return cleared[1:len(cleared)] #wywala wiersz do opisywania danych w tabeli

def segmentSave(saved, SegmentSize): #saved czyli koordynaty x y z do zapisania musi być zapisane także magnitudo i nazwa gwiazdy, SegmentSize wielkość jednego bloku zapisu w Pc
    
    #ułomny algorytm radzę się nie inspirować jutro zobaczę czy usprawnia obliczenia jak tylko znajdę większy set gwiazd
    newpath = os.path.join(os.path.dirname(__file__),"Segments")
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    i = 0   
    for entry in saved:
        if i% 300000==0:
            print(i/300000)
        #ustalenie segmentu do którego przynależą dane koordynaty
        x = int(int(entry[0] - entry[0]%SegmentSize) / SegmentSize)
        y = int(int(entry[1] - entry[1]%SegmentSize) / SegmentSize)
        z = int(int(entry[2] - entry[2]%SegmentSize) / SegmentSize)
        i+=1
        name = (str(hex(x))+"."+str(hex(y))+"."+str(hex(z))).replace("0x","")+".csv"#zamiana numeru segmentu na hex i usunięcie 0x kolejne wartości oddzielone "." mogą być ujemne
        f = open(os.path.join(newpath,name),'a')
        f.write(str(entry).replace(", ",",")+"\n")
        
def check(cleared,threshold):#cleared czyli dane z pliku przepuszczone przez def cleared, threshold po osiągnięciu błędu o tej wartości ten zostaje zlogowany i zwrócony
    notaccepted=[]
    dx=[]
    dz=[]
    dy=[]
    current = []
    for t in cleared:
        current = getDegrees([0,0,0],getCords([float(t[1]),float(t[2]),float(t[3])]))
        #liczenie różnicy między podanymi kątami i odległością a nimi po zamienieniu na koordynaty i znów na kąty
        x = abs(current[0]-float(t[1]))
        y = abs(current[1]-float(t[2]))
        z = abs(current[2]-float(t[3]))
        
        #logowanie danych po osiągnięciu błędu krytycznego
        if x>threshold or y>threshold or z>threshold:
            notaccepted+="new log "+str(t)+"   "+str(current)
            
        #dodanie błędów do tablicy
        dx.append(x)
        dy.append(y)
        dz.append(z)
        
    # liczenie średniej pomyłki oraz maksymalnej
    print("ra "+str(sum(dx)/len(dx))+" max "+str(max(dx)))
    print("dec "+str(sum(dy)/len(dy))+" max "+str(max(dy)))
    print("distance "+str(sum(dz)/len(dz))+" max "+str(max(dz)))
    # zwrot logu
    return notaccepted

print("start")
#czyszczenie danych
cleared = dataClear("ico.csv")
print("cleared")

saved =[]
#zamiana kątów na koordynaty
for t in cleared:
    saved.append(getCords([float(t[1]),float(t[2]),float(t[3])]))
    
print("saved")
# zamiana koordynatów na kąty
for t in saved:
    getDegrees([0,0,0],t)

#sprawdzenie omylności algorytmu
#print(check(cleared,0.001))

#zapisanie do segmentów
#segmentSave(saved,30)