from time import time
from pymongo import MongoClient
import logging
import numpy as np
import os

#name of the model
NAME = "osso spugnoso"
#description of the model
DESCRIPTION = "Modello di un osso spugnoso clusterizzato tramite un partizionatore per coordinate affini"
#dimensions of the first cluster 
WIDTH = 800
HEIGHT = 800
DEPTH = 1024
#threshold of the number of points in a single cluster
POINT_THRESHOLD = 50000




class Point:
    def __init__(self):
        self.id = id
    def setCoordinates(self, x,y,z,w):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)


'''
CODICE PER TRADUZIONE DAL VECCHIO FILE
'''
def loadSlice(in_file, offset):
    fileSlice = []
    in_file.seek(offset)
    in_file.readline() #jump over the comment '#New fileSlice'
    
    for i in range(800):
        fileSlice.append(in_file.readline()[:-2])
            
    #print fileSlice
    #logging.info(fileSlice)
    return fileSlice

def traduciSlice(fileSlice,in_file,z):
    print "Traduco Slice con z "+str(z)
    offset = in_file.tell()
    in_file.seek(offset)
    global linea_counter
    newSlice = ""
    One_Counter = 0
    for y in range(len(fileSlice)):
        elementi = list(fileSlice[y])
        for x in range(len(elementi)):
            if elementi[x] == str(1):
                One_Counter+=1
                newSlice+= ""+str(x)+","+str(y)+","+str(z)+",1|"
                linea_counter+=1
                if linea_counter >= 10000 or x == len(elementi)-1:
                    #print "VADO A CAPO "
                    linea_counter = 0
                    newSlice = newSlice[:-1]
                    newSlice+= "\n"
                    
                
            #print elementi[x]
        
    
    print "ci sono "+str(One_Counter)+" coordinate"
    if One_Counter >0:
        #logging.info(newSlice)
        in_file.write(newSlice)
    

#metodo di test iniziale, genera un file che posso gestire
def translateFile():
    print "Inizio a rimodellare il boneFile"
    boneFile = (open('bone_clean.txt', 'r'))
    newfile = (open('newFile.txt', 'a'))
    for z in range(1024):
        offset = boneFile.tell()
        #logging.info(offset)
        boneSlice = loadSlice(boneFile,offset)
        traduciSlice(boneSlice,newfile,z)
        #ORA TRADUCO LA SLICE
        
        #for y in range(800):
            #for x in range(800):
    
    
    
    #logging.debug('This message should go to the log boneFile')
    #logging.info('So should this')
    #logging.warning('And this, too')
    newfile.close()
    boneFile.close()
    return


'''
FINE CODICE PER TRADUZIONE DAL VECCHIO FILE
'''












'''
PARTIZIONATORE PER COORDINATE AFFINI
'''

def saveModelTree(model_tree):
    print model_tree
    print "...to disk"
    print "saving model_tree..."
    client = MongoClient('localhost', 27017)  
    db = client['db-bio']
    CLUSTERS = db.clusters  
    post = {}
    post["_id"] = "model"
    post["name"] = NAME
    post["description"] = DESCRIPTION
    post["dimensions"] = [WIDTH, HEIGHT, DEPTH]
    post["clusters_tree"] = model_tree
    print post
    CLUSTERS.insert(post)
    print "documents created: ", CLUSTERS.count()


def salvaJSON(JSON):
    client = MongoClient('localhost', 27017)
    db = client['db-bio']
    CLUSTERS = db.clusters
    CLUSTERS.insert(JSON)

def creaJSON(clusterId,TMatrix,clusterFile):
    print "Salvo JSON con id "+str(clusterId)
    logging.info("Salvo JSON con id "+str(clusterId))
    
    TMatrix = TMatrix.tolist()
    #TMatrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
    punti = []
    for line in clusterFile:
        puntiStringArray = line.split("|")
        for puntoStr in puntiStringArray:
            punto = puntoStr.split(",")
            for i in range(4):
                punto[i] = float(punto[i])
                
            #punto.setCoordinates(coordinates[0], coordinates[1], coordinates[2], coordinates[3])
            punti.append(punto)

    
    doc = {}
    doc["_id"] = clusterId
    doc["points"] = punti
    doc["TMatrix"] = TMatrix
    
    salvaJSON(doc)
    clusterFileName = clusterFile.name
    clusterFile.close()
    os.remove(clusterFileName)


def salvaPuntiSuDisco(pointBuffer,subClusterFileName):
    
    stringToWrite = ""
    counter = 0
    total_counter = 0
    
    
    for point in pointBuffer:
        counter += 1
        total_counter+=1
        stringToWrite += str(float(point.x))+","+str(float(point.y))+","+str(float(point.z))+","+str(float(point.w))
        
        if counter == 10000 or total_counter == len(pointBuffer):
            
            print "total counter: "+str(total_counter)+" of "+str(len(pointBuffer))
            counter = 0
            stringToWrite += "\n"
        else:
            stringToWrite += "|"
    
    list([pointBuffer.pop() for z in xrange(len(pointBuffer))])    
    subClusterFile = open(subClusterFileName, 'a')
    subClusterFile.write(stringToWrite)
    subClusterFile.close()
      
    print "salvo i punti sul file "+subClusterFileName

#assegna il punto al giusto cluster
def savePoint(point,clusterFileName):
    
    segni = ""
    if float(point.x)>0:
        segni+=str(1)
    else:
        segni+=str(0)    
    if float(point.y)>0:
        segni+=str(1)
    else:
        segni+=str(0)
    if float(point.z)>0:
        segni+=str(1)
    else:
        segni+=str(0)
    if float(point.w)>0:
        segni+=str(1)
    else:
        segni+=str(0)
        
    subClusterFileName = ""
    pointBuffer = []
    
    if segni == "0000": #teoricamente impossibile dato che la somma delle coordinate deve essere = 1, inserito per completezza
        subClusterFileName = clusterFileName[:-4]+"0000.txt"
        pointBuffer = []
        print "Segno 0000, qualcosa non va"
    elif segni == "0001":
        subClusterFileName = clusterFileName[:-4]+"0001.txt"
        pointBuffer = buffer_0001
    
    elif segni == "0010":
        subClusterFileName = clusterFileName[:-4]+"0010.txt"
        pointBuffer = buffer_0010
        
    elif segni == "0011":
        subClusterFileName = clusterFileName[:-4]+"0011.txt"
        pointBuffer = buffer_0011
        
    elif segni == "0100":
        subClusterFileName = clusterFileName[:-4]+"0100.txt"
        pointBuffer = buffer_0100
        
    elif segni == "0101":
        subClusterFileName = clusterFileName[:-4]+"0101.txt"
        pointBuffer = buffer_0101
        
    elif segni == "0110":
        subClusterFileName = clusterFileName[:-4]+"0110.txt"
        pointBuffer = buffer_0110
        
    elif segni == "0111":
        subClusterFileName = clusterFileName[:-4]+"0111.txt"
        pointBuffer = buffer_0111
        
    elif segni == "1000":
        subClusterFileName = clusterFileName[:-4]+"1000.txt"
        pointBuffer = buffer_1000
        
    elif segni == "1001":
        subClusterFileName = clusterFileName[:-4]+"1001.txt"
        pointBuffer = buffer_1001
        
    elif segni == "1010":
        subClusterFileName = clusterFileName[:-4]+"1010.txt"
        pointBuffer = buffer_1010
        
    elif segni == "1011":
        subClusterFileName = clusterFileName[:-4]+"1011.txt"
        pointBuffer = buffer_1011
        
    elif segni == "1100":
        subClusterFileName = clusterFileName[:-4]+"1100.txt"
        pointBuffer = buffer_1100
        
    elif segni == "1101":
        subClusterFileName = clusterFileName[:-4]+"1101.txt"
        pointBuffer = buffer_1101
        
    elif segni == "1110":
        subClusterFileName = clusterFileName[:-4]+"1110.txt"
        pointBuffer = buffer_1110
        
    elif segni == "1111":
        subClusterFileName = clusterFileName[:-4]+"1111.txt"
        pointBuffer = buffer_1111
        
    pointBuffer.append(point)
     
    if len(pointBuffer)>=50000:
        salvaPuntiSuDisco(pointBuffer,subClusterFileName)
    
    return

#processa un chunk di punti
def processChunk(chunk,TMatrix,clusterFileName):
    
    punti = chunk.split("|")
    
    
    for punto in punti:
        coordinate = punto.split(",")
        coordinate[0] = float(coordinate[0])
        coordinate[1] = float(coordinate[1])
        coordinate[2] = float(coordinate[2])
        coordinate[3] = float(coordinate[3])
        coordinate = np.transpose(coordinate)
        coordinate = np.dot(TMatrix,coordinate)
        coordinate = np.transpose(coordinate)
        
        nuovoPunto = Point()
        nuovoPunto.setCoordinates(float(coordinate[0]), float(coordinate[1]), float(coordinate[2]), float(coordinate[3]))
        savePoint(nuovoPunto,clusterFileName)
          
    
    

def getTMatrixWithPoints(P1,P2,P3,P4):
    #PMatrix = [[P1.x,P1.y,P1.z,P1.w],[P2.x,P2.y,P2.z,P2.w],[P3.x,P3.y,P3.z,P3.w],[P4.x,P4.y,P4.z,P4.w]]
    #PMatrix = np.matrix(np.transpose(PMatrix))
    PMatrix = np.matrix([[P1.x,P2.x,P3.x,P4.x],[P1.y,P2.y,P3.y,P4.y],[P1.z,P2.z,P3.z,P4.z],[P1.w,P2.w,P3.w,P4.w]])
    TMatrix = PMatrix.I
    return TMatrix

def processFile(clusterFileName,TMatrixTotal):
    Tree = []
    print "Processo il clusterFile "+clusterFileName
    clusterFile = open(clusterFileName, 'r')
    line_counter = 1
    num_lines = sum(1 for line in clusterFile)
    
    clusterFile.seek(0)  
    TMatrix = []
    if num_lines > 0:
        counter = 0
        P1 = Point()
        P2 = Point()
        P3 = Point()
        P4 = Point()
        for line in clusterFile:
            if counter == int((num_lines*1)/8):
                P1Array = line.split("|")[0].split(",")
                P1.setCoordinates(P1Array[0], P1Array[1], P1Array[2], P1Array[3])
                #print "P1: "+str(P1Array)+" at line "+str(int((num_lines*1)/8))
            if counter == int((num_lines*3)/8):
                P2Array = line.split("|")[0].split(",")
                P2.setCoordinates(P2Array[0], P2Array[1], P2Array[2], P2Array[3])
                #print "P2: "+str(P2Array)+" at line "+str(int((num_lines*3)/8))
            if counter == int((num_lines*5)/8):
                P3Array = line.split("|")[0].split(",")
                P3.setCoordinates(P3Array[0], P3Array[1], P3Array[2], P3Array[3])
                #print "P3: "+str(P3Array)+" at line "+str(int((num_lines*5)/8))
            if counter == int((num_lines*7)/8):
                P4Array = line.split("|")[0].split(",")
                P4.setCoordinates(P4Array[0], P4Array[1], P4Array[2], P4Array[3])
                #print "P4: "+str(P1Array)+" at line "+str(int((num_lines*7)/8))
            
            counter+=1
            
        TMatrix = getTMatrixWithPoints(P1,P2,P3,P4)
        TMatrixTotal = np.dot(TMatrix,TMatrixTotal)
    
    clusterFile.seek(0)
    for line in clusterFile:
        print clusterFileName+" line "+str(line_counter)+" of "+str(num_lines)
        processChunk(line,TMatrix,clusterFileName)
        line_counter += 1
        
    clusterFile.close()
    
    print "Salvo i punti rimasti"
    
    print str(len(buffer_0001))+" punti per il buffer 0001"
    salvaPuntiSuDisco(buffer_0001,clusterFileName[:-4]+"0001.txt")
    
    print str(len(buffer_0010))+" punti per il buffer 0010"
    salvaPuntiSuDisco(buffer_0010,clusterFileName[:-4]+"0010.txt")
        
    print str(len(buffer_0011))+" punti per il buffer 0011"
    salvaPuntiSuDisco(buffer_0011,clusterFileName[:-4]+"0011.txt")      
    
    print str(len(buffer_0100))+" punti per il buffer 0100"
    salvaPuntiSuDisco(buffer_0100,clusterFileName[:-4]+"0100.txt") 

    print str(len(buffer_0101))+" punti per il buffer 0101"
    salvaPuntiSuDisco(buffer_0101,clusterFileName[:-4]+"0101.txt")
    
    print str(len(buffer_0110))+" punti per il buffer 0110"
    salvaPuntiSuDisco(buffer_0110,clusterFileName[:-4]+"0110.txt")
        
    print str(len(buffer_0111))+" punti per il buffer 0111"
    salvaPuntiSuDisco(buffer_0111,clusterFileName[:-4]+"0111.txt")      
    
    print str(len(buffer_1000))+" punti per il buffer 1000"
    salvaPuntiSuDisco(buffer_1000,clusterFileName[:-4]+"1000.txt") 
    
    print str(len(buffer_1001))+" punti per il buffer 1001"
    salvaPuntiSuDisco(buffer_1001,clusterFileName[:-4]+"1001.txt")
    
    print str(len(buffer_1010))+" punti per il buffer 1010"
    salvaPuntiSuDisco(buffer_1010,clusterFileName[:-4]+"1010.txt")
        
    print str(len(buffer_1011))+" punti per il buffer 1011"
    salvaPuntiSuDisco(buffer_1011,clusterFileName[:-4]+"1011.txt")      
    
    print str(len(buffer_1100))+" punti per il buffer 1100"
    salvaPuntiSuDisco(buffer_1100,clusterFileName[:-4]+"1100.txt") 

    print str(len(buffer_1101))+" punti per il buffer 1101"
    salvaPuntiSuDisco(buffer_1101,clusterFileName[:-4]+"1101.txt")
    
    print str(len(buffer_1110))+" punti per il buffer 1110"
    salvaPuntiSuDisco(buffer_1110,clusterFileName[:-4]+"1110.txt")
        
    print str(len(buffer_1111))+" punti per il buffer 1111"
    salvaPuntiSuDisco(buffer_1111,clusterFileName[:-4]+"1111.txt")
    
    
    #ora vado ricorsivamente sui subClusters
    P1 = Point()
    P2 = Point()
    P3 = Point()
    P4 = Point()
    
    fileName = clusterFileName[:-4]+"0001.txt"
    clusterFile = open(fileName,'r')
    num_lines = sum(1 for line in clusterFile)
    clusterFile.close()

    fileNameComponents = fileName[:-4].split("_")
    clusterId = fileNameComponents[-1] #ultimo elemento dell'array
    Tree.append(clusterId)
    
    if num_lines > POINT_THRESHOLD/10000:
        print "Ci sono piu' di "+str(POINT_THRESHOLD)+"punti nel subCluster 0001"
        subTree = processFile(fileName,TMatrixTotal)
        Tree.append(subTree)
    else:
        clusterFile = open(fileName,'r')
        creaJSON(clusterId,TMatrixTotal,clusterFile)
        clusterFile.close()
        logging.info("chiuso il cluster "+fileName+" con "+str(num_lines*10000)+" punti circa\nTMatrixTotal:\n"+str(TMatrixTotal)+"\n\n")
        print "CLUSTER 0001 CHIUSO, DOVREI GENERARE JSON"
        
    
    fileName = clusterFileName[:-4]+"0010.txt"
    clusterFile = open(fileName,'r')
    num_lines = sum(1 for line in clusterFile)
    clusterFile.close()
    
    fileNameComponents = fileName[:-4].split("_")
    clusterId = fileNameComponents[-1] #ultimo elemento dell'array
    print "Cluster ID: "+clusterId
    logging.info("Cluster ID: "+clusterId)
    Tree.append(clusterId)
    if num_lines > POINT_THRESHOLD/10000:
        print "Ci sono piu' di "+str(POINT_THRESHOLD)+"punti nel subCluster 0010"
        subTree = processFile(fileName,TMatrixTotal)
        Tree.append(subTree)
    else:
        
        clusterFile = open(fileName,'r')
        creaJSON(clusterId,TMatrixTotal,clusterFile)
        clusterFile.close()
        
        logging.info("chiuso il cluster "+fileName+" con "+str(num_lines*10000)+" punti circa\nTMatrixTotal:\n"+str(TMatrixTotal)+"\n\n")
        
        print "CLUSTER 0010 CHIUSO, DOVREI GENERARE JSON"
        
        
    fileName = clusterFileName[:-4]+"0011.txt"
    clusterFile = open(fileName,'r')
    num_lines = sum(1 for line in clusterFile)
    clusterFile.close()
    
    fileNameComponents = fileName[:-4].split("_")
    clusterId = fileNameComponents[-1] #ultimo elemento dell'array
    Tree.append(clusterId)
    if num_lines > POINT_THRESHOLD/10000:
        print "Ci sono piu' di "+ str(POINT_THRESHOLD) +" punti nel subCluster 0011"
        subTree = processFile(fileName,TMatrixTotal)
        Tree.append(subTree)
    else:

        clusterFile = open(fileName,'r')
        creaJSON(clusterId,TMatrixTotal,clusterFile)
        clusterFile.close()
        
        logging.info("chiuso il cluster "+fileName+" con "+str(num_lines*10000)+" punti circa\nTMatrixTotal:\n"+str(TMatrixTotal)+"\n\n")
        print "CLUSTER 0011 CHIUSO, DOVREI GENERARE JSON"
        
    fileName = clusterFileName[:-4]+"0100.txt"
    clusterFile = open(fileName,'r')
    num_lines = sum(1 for line in clusterFile)
    clusterFile.close()
    
    fileNameComponents = fileName[:-4].split("_")
    clusterId = fileNameComponents[-1] #ultimo elemento dell'array
    Tree.append(clusterId)
    if num_lines > POINT_THRESHOLD/10000:
        print "Ci sono piu' di "+ str(POINT_THRESHOLD) +" punti nel subCluster 0100"
        subTree = processFile(fileName,TMatrixTotal)
        Tree.append(subTree)
    else:
    
        clusterFile = open(fileName,'r')
        creaJSON(clusterId,TMatrixTotal,clusterFile)
        clusterFile.close()
        
        logging.info("chiuso il cluster "+fileName+" con "+str(num_lines*10000)+" punti circa\nTMatrixTotal:\n"+str(TMatrixTotal)+"\n\n")
        print "CLUSTER 0100 CHIUSO, DOVREI GENERARE JSON"
        
    
    fileName = clusterFileName[:-4]+"0101.txt"
    clusterFile = open(fileName,'r')
    num_lines = sum(1 for line in clusterFile)
    clusterFile.close()
    
    fileNameComponents = fileName[:-4].split("_")
    clusterId = fileNameComponents[-1] #ultimo elemento dell'array
    Tree.append(clusterId)
    if num_lines > POINT_THRESHOLD/10000:
        print "Ci sono piu' di "+ str(POINT_THRESHOLD) +" punti nel subCluster 0101"
        subTree = processFile(fileName,TMatrixTotal)
        Tree.append(subTree)
    else:
        

        clusterFile = open(fileName,'r')
        creaJSON(clusterId,TMatrixTotal,clusterFile)
        clusterFile.close()
        
        logging.info("chiuso il cluster "+fileName+" con "+str(num_lines*10000)+" punti circa\nTMatrixTotal:\n"+str(TMatrixTotal)+"\n\n")
        print "CLUSTER 0101 CHIUSO, DOVREI GENERARE JSON"
        
    
    fileName = clusterFileName[:-4]+"0110.txt"
    clusterFile = open(fileName,'r')
    num_lines = sum(1 for line in clusterFile)
    clusterFile.close()
    
    fileNameComponents = fileName[:-4].split("_")
    clusterId = fileNameComponents[-1] #ultimo elemento dell'array
    Tree.append(clusterId)
    if num_lines > POINT_THRESHOLD/10000:
        print "Ci sono piu' di "+ str(POINT_THRESHOLD) +" punti nel subCluster 0110"
        subTree = processFile(fileName,TMatrixTotal)
        Tree.append(subTree)
    else:
        
        clusterFile = open(fileName,'r')
        creaJSON(clusterId,TMatrixTotal,clusterFile)
        clusterFile.close()
        
        logging.info("chiuso il cluster "+fileName+" con "+str(num_lines*10000)+" punti circa\nTMatrixTotal:\n"+str(TMatrixTotal)+"\n\n")
        print "CLUSTER 0110 CHIUSO, DOVREI GENERARE JSON"
        
    
    fileName = clusterFileName[:-4]+"0111.txt"
    clusterFile = open(fileName,'r')
    num_lines = sum(1 for line in clusterFile)
    clusterFile.close()
    
    fileNameComponents = fileName[:-4].split("_")
    clusterId = fileNameComponents[-1] #ultimo elemento dell'array
    Tree.append(clusterId)
    if num_lines > POINT_THRESHOLD/10000:
        print "Ci sono piu' di "+ str(POINT_THRESHOLD) +" punti nel subCluster 0111"
        subTree = processFile(fileName,TMatrixTotal)
        Tree.append(subTree)
    else:
        
        clusterFile = open(fileName,'r')
        creaJSON(clusterId,TMatrixTotal,clusterFile)
        clusterFile.close()
        
        logging.info("chiuso il cluster "+fileName+" con "+str(num_lines*10000)+" punti circa\nTMatrixTotal:\n"+str(TMatrixTotal)+"\n\n")
        print "CLUSTER 0111 CHIUSO, DOVREI GENERARE JSON"
        
        
    fileName = clusterFileName[:-4]+"1000.txt"
    clusterFile = open(fileName,'r')
    num_lines = sum(1 for line in clusterFile)
    clusterFile.close()
    
    fileNameComponents = fileName[:-4].split("_")
    clusterId = fileNameComponents[-1] #ultimo elemento dell'array
    Tree.append(clusterId)
    if num_lines > POINT_THRESHOLD/10000:
        print "Ci sono piu' di "+ str(POINT_THRESHOLD) +" punti nel subCluster 1000"
        subTree = processFile(fileName,TMatrixTotal)
        Tree.append(subTree)
    else:
    
        clusterFile = open(fileName,'r')
        creaJSON(clusterId,TMatrixTotal,clusterFile)
        clusterFile.close()
        
        logging.info("chiuso il cluster "+fileName+" con "+str(num_lines*10000)+" punti circa\nTMatrixTotal:\n"+str(TMatrixTotal)+"\n\n")
        print "CLUSTER 1000 CHIUSO, DOVREI GENERARE JSON"
        
        
    #---------
    
    fileName = clusterFileName[:-4]+"1001.txt"
    clusterFile = open(fileName,'r')
    num_lines = sum(1 for line in clusterFile)
    clusterFile.close()
    
    fileNameComponents = fileName[:-4].split("_")
    clusterId = fileNameComponents[-1] #ultimo elemento dell'array
    Tree.append(clusterId)
    if num_lines > POINT_THRESHOLD/10000:
        print "Ci sono piu' di "+ str(POINT_THRESHOLD) +" punti nel subCluster 1001"
        subTree = processFile(fileName,TMatrixTotal)
        Tree.append(subTree)
    else:
        
        clusterFile = open(fileName,'r')
        creaJSON(clusterId,TMatrixTotal,clusterFile)
        clusterFile.close()
        
        logging.info("chiuso il cluster "+fileName+" con "+str(num_lines*10000)+" punti circa\nTMatrixTotal:\n"+str(TMatrixTotal)+"\n\n")
        print "CLUSTER 1001 CHIUSO, DOVREI GENERARE JSON"
        
    
    fileName = clusterFileName[:-4]+"1010.txt"
    clusterFile = open(fileName,'r')
    num_lines = sum(1 for line in clusterFile)
    clusterFile.close()
    
    fileNameComponents = fileName[:-4].split("_")
    clusterId = fileNameComponents[-1] #ultimo elemento dell'array
    Tree.append(clusterId)
    if num_lines > POINT_THRESHOLD/10000:
        print "Ci sono piu' di "+ str(POINT_THRESHOLD) +" punti nel subCluster 1010"
        subTree = processFile(fileName,TMatrixTotal)
        Tree.append(subTree)
    else:
        
        clusterFile = open(fileName,'r')
        creaJSON(clusterId,TMatrixTotal,clusterFile)
        clusterFile.close()
        
        logging.info("chiuso il cluster "+fileName+" con "+str(num_lines*10000)+" punti circa\nTMatrixTotal:\n"+str(TMatrixTotal)+"\n\n")
        print "CLUSTER 1010 CHIUSO, DOVREI GENERARE JSON"
            
        
        
    fileName = clusterFileName[:-4]+"1011.txt"
    clusterFile = open(fileName,'r')
    num_lines = sum(1 for line in clusterFile)
    clusterFile.close()
    
    fileNameComponents = fileName[:-4].split("_")
    clusterId = fileNameComponents[-1] #ultimo elemento dell'array
    Tree.append(clusterId)
    if num_lines > POINT_THRESHOLD/10000:
        print "Ci sono piu' di "+ str(POINT_THRESHOLD) +" punti nel subCluster 1011"
        subTree = processFile(fileName,TMatrixTotal)
        Tree.append(subTree)
    else:
        
        clusterFile = open(fileName,'r')
        creaJSON(clusterId,TMatrixTotal,clusterFile)
        clusterFile.close()
        
        logging.info("chiuso il cluster "+fileName+" con "+str(num_lines*10000)+" punti circa\nTMatrixTotal:\n"+str(TMatrixTotal)+"\n\n")
        print "CLUSTER 1011 CHIUSO, DOVREI GENERARE JSON"
        
    fileName = clusterFileName[:-4]+"1100.txt"
    clusterFile = open(fileName,'r')
    num_lines = sum(1 for line in clusterFile)
    clusterFile.close()
    
    fileNameComponents = fileName[:-4].split("_")
    clusterId = fileNameComponents[-1] #ultimo elemento dell'array
    Tree.append(clusterId)
    if num_lines > POINT_THRESHOLD/10000:
        print "Ci sono piu' di "+ str(POINT_THRESHOLD) +" punti nel subCluster 1100"
        subTree = processFile(fileName,TMatrixTotal)
        Tree.append(subTree)
    else:
        
        clusterFile = open(fileName,'r')
        creaJSON(clusterId,TMatrixTotal,clusterFile)
        clusterFile.close()
        
        logging.info("chiuso il cluster "+fileName+" con "+str(num_lines*10000)+" punti circa\nTMatrixTotal:\n"+str(TMatrixTotal)+"\n\n")
        print "CLUSTER 1100 CHIUSO, DOVREI GENERARE JSON"
        
    
    fileName = clusterFileName[:-4]+"1101.txt"
    clusterFile = open(fileName,'r')
    num_lines = sum(1 for line in clusterFile)
    clusterFile.close()
    
    fileNameComponents = fileName[:-4].split("_")
    clusterId = fileNameComponents[-1] #ultimo elemento dell'array
    Tree.append(clusterId)
    if num_lines > POINT_THRESHOLD/10000:
        print "Ci sono piu' di "+ str(POINT_THRESHOLD) +" punti nel subCluster 1101"
        subTree = processFile(fileName,TMatrixTotal)
        Tree.append(subTree)
    else:
        
        clusterFile = open(fileName,'r')
        creaJSON(clusterId,TMatrixTotal,clusterFile)
        clusterFile.close()
        
        logging.info("chiuso il cluster "+fileName+" con "+str(num_lines*10000)+" punti circa\nTMatrixTotal:\n"+str(TMatrixTotal)+"\n\n")
        print "CLUSTER 1101 CHIUSO, DOVREI GENERARE JSON"
        
    
    fileName = clusterFileName[:-4]+"1110.txt"
    clusterFile = open(fileName,'r')
    num_lines = sum(1 for line in clusterFile)
    clusterFile.close()
    
    fileNameComponents = fileName[:-4].split("_")
    clusterId = fileNameComponents[-1] #ultimo elemento dell'array
    Tree.append(clusterId)
    if num_lines > POINT_THRESHOLD/10000:
        print "Ci sono piu' di "+ str(POINT_THRESHOLD) +" punti nel subCluster 1110"
        subTree = processFile(fileName,TMatrixTotal)
        Tree.append(subTree)
    else:
        
        clusterFile = open(fileName,'r')
        creaJSON(clusterId,TMatrixTotal,clusterFile)
        clusterFile.close()
        
        logging.info("chiuso il cluster "+fileName+" con "+str(num_lines*10000)+" punti circa\nTMatrixTotal:\n"+str(TMatrixTotal)+"\n\n")
        print "CLUSTER 1110 CHIUSO, DOVREI GENERARE JSON"
        
    
    fileName = clusterFileName[:-4]+"1111.txt"
    clusterFile = open(fileName,'r')
    num_lines = sum(1 for line in clusterFile)
    clusterFile.close()
    
    fileNameComponents = fileName[:-4].split("_")
    clusterId = fileNameComponents[-1] #ultimo elemento dell'array
    Tree.append(clusterId)
    if num_lines > POINT_THRESHOLD/10000:
        print "Ci sono piu' di "+ str(POINT_THRESHOLD) +" punti nel subCluster 1111"
        subTree = processFile(fileName,TMatrixTotal)
        Tree.append(subTree)
    else:

        clusterFile = open(fileName,'r')
        creaJSON(clusterId,TMatrixTotal,clusterFile)
        clusterFile.close()
        
        logging.info("chiuso il cluster "+fileName+" con "+str(num_lines*10000)+" punti circa\nTMatrixTotal:\n"+str(TMatrixTotal)+"\n\n")
        print "CLUSTER 1111 CHIUSO, DOVREI GENERARE JSON"
    
    
    #verifica nome cluster
    clusterNameSplit = clusterFileName[:-4].split("_")
    if clusterNameSplit[2] != "":
        logging.warning("Cancello il clusterFile "+clusterFileName)
        os.remove(clusterFileName)
    
    print "Albero: "+str(Tree)
    return Tree
        
def getStart():
    
    client = MongoClient('localhost', 27017)
    db = client['db-bio']
    db.drop_collection('clusters')
    
    
    #creo una matrice identita' che servira' per formare la matrice di trasformazione totale per ogni cluster
    
    P1 = Point()
    P1.x = 1
    P1.y = 0
    P1.z = 0
    P1.w = 0
    
    P2 = Point()
    P2.x = 0
    P2.y = 1
    P2.z = 0
    P2.w = 0
    
    P3 = Point()
    P3.x = 0
    P3.y = 0
    P3.z = 1
    P3.w = 0
    
    P4 = Point()
    P4.x = 0
    P4.y = 0
    P4.z = 0
    P4.w = 1
    
    
    
    TMatrixTotal = getTMatrixWithPoints(P1,P2,P3,P4)
    
    
    fileName = "bone_4D_.txt"
    model_tree = processFile(fileName,TMatrixTotal)
    
    saveModelTree(model_tree)
    logging.info("Model Tree: "+str(model_tree))
    
    
    #model_tree = ['0001', '0010', ['00100001', '00100010', '00100011', '00100100', '00100101', '00100110', ['001001100001', '001001100010', '001001100011', '001001100100', '001001100101', '001001100110', '001001100111', '001001101000', '001001101001', '001001101010', '001001101011', '001001101100', '001001101101', '001001101110', '001001101111'], '00100111', '00101000', '00101001', '00101010', '00101011', '00101100', '00101101', '00101110', '00101111'], '0011', '0100', ['01000001', '01000010', '01000011', ['010000110001', '010000110010', '010000110011', '010000110100', '010000110101', '010000110110', '010000110111', '010000111000', '010000111001', '010000111010', '010000111011', '010000111100', '010000111101', '010000111110', '010000111111'], '01000100', '01000101', ['010001010001', '010001010010', '010001010011', '010001010100', '010001010101', '010001010110', '010001010111', '010001011000', '010001011001', '010001011010', '010001011011', '010001011100', '010001011101', '010001011110', '010001011111'], '01000110', '01000111', ['010001110001', '010001110010', '010001110011', '010001110100', '010001110101', '010001110110', '010001110111', '010001111000', '010001111001', '010001111010', '010001111011', ['0100011110110001', '0100011110110010', '0100011110110011', '0100011110110100', '0100011110110101', '0100011110110110', '0100011110110111', '0100011110111000', '0100011110111001', '0100011110111010', '0100011110111011', '0100011110111100', '0100011110111101', '0100011110111110', '0100011110111111'], '010001111100', '010001111101', '010001111110', '010001111111'], '01001000', '01001001', '01001010', ['010010100001', '010010100010', '010010100011', '010010100100', '010010100101', '010010100110', '010010100111', '010010101000', '010010101001', '010010101010', '010010101011', '010010101100', '010010101101', '010010101110', '010010101111'], '01001011', ['010010110001', '010010110010', '010010110011', '010010110100', '010010110101', '010010110110', '010010110111', '010010111000', '010010111001', '010010111010', '010010111011', '010010111100', '010010111101', '010010111110', '010010111111'], '01001100', ['010011000001', '010011000010', '010011000011', '010011000100', '010011000101', '010011000110', '010011000111', '010011001000', '010011001001', '010011001010', '010011001011', '010011001100', '010011001101', '010011001110', '010011001111'], '01001101', ['010011010001', '010011010010', '010011010011', '010011010100', '010011010101', '010011010110', '010011010111', '010011011000', '010011011001', '010011011010', '010011011011', '010011011100', '010011011101', '010011011110', '010011011111'], '01001110', ['010011100001', '010011100010', '010011100011', '010011100100', '010011100101', '010011100110', '010011100111', '010011101000', '010011101001', '010011101010', '010011101011', '010011101100', '010011101101', '010011101110', '010011101111'], '01001111', ['010011110001', '010011110010', '010011110011', '010011110100', '010011110101', '010011110110', '010011110111', '010011111000', '010011111001', '010011111010', '010011111011', '010011111100', '010011111101', '010011111110', '010011111111']], '0101', ['01010001', '01010010', '01010011', '01010100', '01010101', ['010101010001', '010101010010', '010101010011', '010101010100', '010101010101', '010101010110', '010101010111', '010101011000', '010101011001', '010101011010', '010101011011', '010101011100', '010101011101', '010101011110', '010101011111'], '01010110', ['010101100001', '010101100010', '010101100011', '010101100100', '010101100101', '010101100110', '010101100111', '010101101000', '010101101001', '010101101010', '010101101011', '010101101100', '010101101101', '010101101110', '010101101111'], '01010111', ['010101110001', '010101110010', '010101110011', '010101110100', '010101110101', '010101110110', '010101110111', '010101111000', '010101111001', '010101111010', '010101111011', ['0101011110110001', '0101011110110010', '0101011110110011', '0101011110110100', '0101011110110101', '0101011110110110', '0101011110110111', '0101011110111000', '0101011110111001', '0101011110111010', '0101011110111011', '0101011110111100', '0101011110111101', '0101011110111110', '0101011110111111'], '010101111100', '010101111101', '010101111110', '010101111111'], '01011000', '01011001', ['010110010001', '010110010010', '010110010011', '010110010100', '010110010101', '010110010110', ['0101100101100001', '0101100101100010', '0101100101100011', '0101100101100100', '0101100101100101', '0101100101100110', '0101100101100111', '0101100101101000', '0101100101101001', '0101100101101010', '0101100101101011', '0101100101101100', '0101100101101101', '0101100101101110', '0101100101101111'], '010110010111', '010110011000', '010110011001', ['0101100110010001', '0101100110010010', '0101100110010011', '0101100110010100', '0101100110010101', '0101100110010110', ['01011001100101100001', '01011001100101100010', '01011001100101100011', '01011001100101100100', '01011001100101100101', '01011001100101100110', '01011001100101100111', '01011001100101101000', '01011001100101101001', '01011001100101101010', '01011001100101101011', '01011001100101101100', '01011001100101101101', '01011001100101101110', '01011001100101101111'], '0101100110010111', '0101100110011000', '0101100110011001', '0101100110011010', '0101100110011011', '0101100110011100', '0101100110011101', ['01011001100111010001', '01011001100111010010', '01011001100111010011', '01011001100111010100', '01011001100111010101', '01011001100111010110', '01011001100111010111', '01011001100111011000', '01011001100111011001', '01011001100111011010', '01011001100111011011', '01011001100111011100', '01011001100111011101', '01011001100111011110', '01011001100111011111'], '0101100110011110', '0101100110011111'], '010110011010', '010110011011', '010110011100', '010110011101', '010110011110', '010110011111'], '01011010', ['010110100001', '010110100010', '010110100011', '010110100100', '010110100101', '010110100110', '010110100111', '010110101000', '010110101001', ['0101101010010001', '0101101010010010', '0101101010010011', '0101101010010100', '0101101010010101', '0101101010010110', '0101101010010111', '0101101010011000', '0101101010011001', '0101101010011010', '0101101010011011', '0101101010011100', '0101101010011101', '0101101010011110', '0101101010011111'], '010110101010', '010110101011', '010110101100', '010110101101', '010110101110', '010110101111'], '01011011', ['010110110001', '010110110010', '010110110011', '010110110100', '010110110101', '010110110110', '010110110111', '010110111000', '010110111001', '010110111010', '010110111011', ['0101101110110001', '0101101110110010', '0101101110110011', '0101101110110100', '0101101110110101', '0101101110110110', '0101101110110111', '0101101110111000', '0101101110111001', '0101101110111010', '0101101110111011', '0101101110111100', '0101101110111101', '0101101110111110', '0101101110111111'], '010110111100', '010110111101', '010110111110', '010110111111'], '01011100', '01011101', ['010111010001', '010111010010', '010111010011', '010111010100', '010111010101', '010111010110', '010111010111', '010111011000', '010111011001', '010111011010', '010111011011', '010111011100', '010111011101', '010111011110', '010111011111'], '01011110', ['010111100001', '010111100010', '010111100011', '010111100100', '010111100101', '010111100110', '010111100111', '010111101000', '010111101001', '010111101010', '010111101011', ['0101111010110001', '0101111010110010', '0101111010110011', '0101111010110100', '0101111010110101', '0101111010110110', '0101111010110111', '0101111010111000', '0101111010111001', '0101111010111010', '0101111010111011', '0101111010111100', '0101111010111101', '0101111010111110', '0101111010111111'], '010111101100', '010111101101', '010111101110', '010111101111'], '01011111'], '0110', ['01100001', '01100010', '01100011', '01100100', '01100101', ['011001010001', '011001010010', '011001010011', '011001010100', '011001010101', '011001010110', '011001010111', '011001011000', '011001011001', '011001011010', '011001011011', '011001011100', '011001011101', ['0110010111010001', '0110010111010010', '0110010111010011', '0110010111010100', '0110010111010101', '0110010111010110', '0110010111010111', '0110010111011000', '0110010111011001', '0110010111011010', '0110010111011011', '0110010111011100', '0110010111011101', '0110010111011110', '0110010111011111'], '011001011110', '011001011111'], '01100110', ['011001100001', '011001100010', '011001100011', '011001100100', '011001100101', '011001100110', '011001100111', '011001101000', '011001101001', '011001101010', '011001101011', '011001101100', '011001101101', '011001101110', '011001101111'], '01100111', ['011001110001', '011001110010', '011001110011', '011001110100', '011001110101', '011001110110', '011001110111', '011001111000', '011001111001', '011001111010', '011001111011', '011001111100', '011001111101', '011001111110', '011001111111'], '01101000', '01101001', ['011010010001', '011010010010', '011010010011', '011010010100', ['0110100101000001', '0110100101000010', '0110100101000011', '0110100101000100', '0110100101000101', '0110100101000110', '0110100101000111', '0110100101001000', '0110100101001001', '0110100101001010', '0110100101001011', '0110100101001100', '0110100101001101', '0110100101001110', '0110100101001111'], '011010010101', '011010010110', '011010010111', '011010011000', '011010011001', '011010011010', '011010011011', ['0110100110110001', '0110100110110010', '0110100110110011', '0110100110110100', '0110100110110101', '0110100110110110', '0110100110110111', '0110100110111000', '0110100110111001', ['01101001101110010001', '01101001101110010010', '01101001101110010011', '01101001101110010100', '01101001101110010101', '01101001101110010110', '01101001101110010111', '01101001101110011000', '01101001101110011001', '01101001101110011010', '01101001101110011011', '01101001101110011100', '01101001101110011101', '01101001101110011110', '01101001101110011111'], '0110100110111010', '0110100110111011', '0110100110111100', '0110100110111101', '0110100110111110', '0110100110111111'], '011010011100', '011010011101', '011010011110', '011010011111'], '01101010', ['011010100001', '011010100010', '011010100011', '011010100100', '011010100101', '011010100110', '011010100111', '011010101000', '011010101001', '011010101010', '011010101011', ['0110101010110001', '0110101010110010', '0110101010110011', '0110101010110100', '0110101010110101', '0110101010110110', '0110101010110111', '0110101010111000', '0110101010111001', '0110101010111010', '0110101010111011', '0110101010111100', '0110101010111101', '0110101010111110', '0110101010111111'], '011010101100', '011010101101', ['0110101011010001', '0110101011010010', '0110101011010011', '0110101011010100', '0110101011010101', '0110101011010110', '0110101011010111', '0110101011011000', '0110101011011001', '0110101011011010', '0110101011011011', '0110101011011100', '0110101011011101', '0110101011011110', '0110101011011111'], '011010101110', '011010101111'], '01101011', ['011010110001', '011010110010', '011010110011', '011010110100', '011010110101', '011010110110', '011010110111', '011010111000', '011010111001', '011010111010', '011010111011', '011010111100', '011010111101', '011010111110', '011010111111'], '01101100', '01101101', ['011011010001', '011011010010', '011011010011', '011011010100', '011011010101', ['0110110101010001', '0110110101010010', '0110110101010011', '0110110101010100', '0110110101010101', '0110110101010110', ['01101101010101100001', '01101101010101100010', '01101101010101100011', '01101101010101100100', '01101101010101100101', '01101101010101100110', '01101101010101100111', '01101101010101101000', '01101101010101101001', '01101101010101101010', '01101101010101101011', '01101101010101101100', '01101101010101101101', '01101101010101101110', '01101101010101101111'], '0110110101010111', '0110110101011000', '0110110101011001', ['01101101010110010001', '01101101010110010010', '01101101010110010011', '01101101010110010100', '01101101010110010101', '01101101010110010110', '01101101010110010111', '01101101010110011000', '01101101010110011001', '01101101010110011010', '01101101010110011011', '01101101010110011100', '01101101010110011101', '01101101010110011110', '01101101010110011111'], '0110110101011010', '0110110101011011', ['01101101010110110001', '01101101010110110010', '01101101010110110011', '01101101010110110100', '01101101010110110101', '01101101010110110110', '01101101010110110111', '01101101010110111000', '01101101010110111001', '01101101010110111010', '01101101010110111011', '01101101010110111100', '01101101010110111101', '01101101010110111110', '01101101010110111111'], '0110110101011100', '0110110101011101', '0110110101011110', '0110110101011111'], '011011010110', ['0110110101100001', '0110110101100010', '0110110101100011', '0110110101100100', '0110110101100101', '0110110101100110', '0110110101100111', '0110110101101000', '0110110101101001', '0110110101101010', '0110110101101011', '0110110101101100', '0110110101101101', '0110110101101110', '0110110101101111'], '011011010111', ['0110110101110001', '0110110101110010', '0110110101110011', '0110110101110100', '0110110101110101', '0110110101110110', '0110110101110111', '0110110101111000', '0110110101111001', '0110110101111010', '0110110101111011', '0110110101111100', '0110110101111101', '0110110101111110', '0110110101111111'], '011011011000', '011011011001', ['0110110110010001', '0110110110010010', '0110110110010011', '0110110110010100', '0110110110010101', '0110110110010110', '0110110110010111', '0110110110011000', '0110110110011001', '0110110110011010', '0110110110011011', '0110110110011100', '0110110110011101', '0110110110011110', '0110110110011111'], '011011011010', '011011011011', ['0110110110110001', '0110110110110010', '0110110110110011', '0110110110110100', '0110110110110101', '0110110110110110', '0110110110110111', '0110110110111000', '0110110110111001', '0110110110111010', '0110110110111011', '0110110110111100', '0110110110111101', '0110110110111110', '0110110110111111'], '011011011100', '011011011101', ['0110110111010001', '0110110111010010', '0110110111010011', '0110110111010100', '0110110111010101', '0110110111010110', ['01101101110101100001', '01101101110101100010', '01101101110101100011', '01101101110101100100', '01101101110101100101', '01101101110101100110', '01101101110101100111', '01101101110101101000', '01101101110101101001', '01101101110101101010', '01101101110101101011', '01101101110101101100', '01101101110101101101', '01101101110101101110', '01101101110101101111'], '0110110111010111', '0110110111011000', '0110110111011001', ['01101101110110010001', '01101101110110010010', '01101101110110010011', '01101101110110010100', '01101101110110010101', '01101101110110010110', '01101101110110010111', '01101101110110011000', '01101101110110011001', '01101101110110011010', '01101101110110011011', '01101101110110011100', '01101101110110011101', ['011011011101100111010001', '011011011101100111010010', '011011011101100111010011', '011011011101100111010100', '011011011101100111010101', '011011011101100111010110', '011011011101100111010111', '011011011101100111011000', '011011011101100111011001', '011011011101100111011010', '011011011101100111011011', '011011011101100111011100', '011011011101100111011101', '011011011101100111011110', '011011011101100111011111'], '01101101110110011110', '01101101110110011111'], '0110110111011010', '0110110111011011', '0110110111011100', '0110110111011101', ['01101101110111010001', '01101101110111010010', '01101101110111010011', '01101101110111010100', '01101101110111010101', '01101101110111010110', '01101101110111010111', '01101101110111011000', '01101101110111011001', '01101101110111011010', '01101101110111011011', '01101101110111011100', '01101101110111011101', '01101101110111011110', '01101101110111011111'], '0110110111011110', ['01101101110111100001', '01101101110111100010', '01101101110111100011', '01101101110111100100', '01101101110111100101', '01101101110111100110', '01101101110111100111', '01101101110111101000', '01101101110111101001', '01101101110111101010', '01101101110111101011', '01101101110111101100', '01101101110111101101', '01101101110111101110', '01101101110111101111'], '0110110111011111'], '011011011110', '011011011111'], '01101110', ['011011100001', '011011100010', '011011100011', '011011100100', '011011100101', '011011100110', ['0110111001100001', '0110111001100010', '0110111001100011', '0110111001100100', ['01101110011001000001', '01101110011001000010', '01101110011001000011', '01101110011001000100', '01101110011001000101', '01101110011001000110', '01101110011001000111', '01101110011001001000', '01101110011001001001', '01101110011001001010', '01101110011001001011', '01101110011001001100', '01101110011001001101', '01101110011001001110', '01101110011001001111'], '0110111001100101', '0110111001100110', '0110111001100111', '0110111001101000', '0110111001101001', '0110111001101010', '0110111001101011', ['01101110011010110001', '01101110011010110010', '01101110011010110011', '01101110011010110100', '01101110011010110101', '01101110011010110110', '01101110011010110111', '01101110011010111000', '01101110011010111001', '01101110011010111010', '01101110011010111011', '01101110011010111100', '01101110011010111101', '01101110011010111110', '01101110011010111111'], '0110111001101100', '0110111001101101', '0110111001101110', '0110111001101111'], '011011100111', '011011101000', '011011101001', '011011101010', '011011101011', '011011101100', '011011101101', '011011101110', '011011101111'], '01101111'], '0111', ['01110001', '01110010', '01110011', '01110100', '01110101', '01110110', ['011101100001', '011101100010', '011101100011', '011101100100', '011101100101', '011101100110', '011101100111', '011101101000', '011101101001', '011101101010', ['0111011010100001', '0111011010100010', '0111011010100011', '0111011010100100', '0111011010100101', '0111011010100110', '0111011010100111', '0111011010101000', '0111011010101001', '0111011010101010', '0111011010101011', '0111011010101100', '0111011010101101', '0111011010101110', '0111011010101111'], '011101101011', '011101101100', '011101101101', '011101101110', '011101101111'], '01110111', '01111000', '01111001', ['011110010001', '011110010010', '011110010011', '011110010100', '011110010101', '011110010110', '011110010111', '011110011000', '011110011001', '011110011010', '011110011011', '011110011100', '011110011101', '011110011110', '011110011111'], '01111010', '01111011', '01111100', '01111101', '01111110', '01111111'], '1000', '1001', ['10010001', '10010010', '10010011', '10010100', '10010101', '10010110', ['100101100001', '100101100010', '100101100011', '100101100100', '100101100101', '100101100110', ['1001011001100001', '1001011001100010', '1001011001100011', '1001011001100100', '1001011001100101', '1001011001100110', '1001011001100111', '1001011001101000', '1001011001101001', '1001011001101010', '1001011001101011', '1001011001101100', '1001011001101101', '1001011001101110', '1001011001101111'], '100101100111', ['1001011001110001', '1001011001110010', '1001011001110011', '1001011001110100', '1001011001110101', '1001011001110110', ['10010110011101100001', '10010110011101100010', '10010110011101100011', '10010110011101100100', '10010110011101100101', '10010110011101100110', '10010110011101100111', '10010110011101101000', '10010110011101101001', '10010110011101101010', '10010110011101101011', ['100101100111011010110001', '100101100111011010110010', '100101100111011010110011', '100101100111011010110100', '100101100111011010110101', '100101100111011010110110', '100101100111011010110111', '100101100111011010111000', '100101100111011010111001', '100101100111011010111010', '100101100111011010111011', '100101100111011010111100', '100101100111011010111101', '100101100111011010111110', '100101100111011010111111'], '10010110011101101100', '10010110011101101101', '10010110011101101110', '10010110011101101111'], '1001011001110111', '1001011001111000', '1001011001111001', '1001011001111010', '1001011001111011', '1001011001111100', '1001011001111101', '1001011001111110', '1001011001111111'], '100101101000', '100101101001', ['1001011010010001', '1001011010010010', '1001011010010011', '1001011010010100', '1001011010010101', '1001011010010110', '1001011010010111', '1001011010011000', '1001011010011001', '1001011010011010', '1001011010011011', ['10010110100110110001', '10010110100110110010', '10010110100110110011', '10010110100110110100', '10010110100110110101', '10010110100110110110', '10010110100110110111', '10010110100110111000', '10010110100110111001', '10010110100110111010', '10010110100110111011', '10010110100110111100', '10010110100110111101', '10010110100110111110', '10010110100110111111'], '1001011010011100', '1001011010011101', '1001011010011110', '1001011010011111'], '100101101010', '100101101011', ['1001011010110001', '1001011010110010', '1001011010110011', '1001011010110100', '1001011010110101', '1001011010110110', '1001011010110111', '1001011010111000', '1001011010111001', '1001011010111010', '1001011010111011', '1001011010111100', '1001011010111101', '1001011010111110', '1001011010111111'], '100101101100', '100101101101', ['1001011011010001', '1001011011010010', '1001011011010011', '1001011011010100', '1001011011010101', '1001011011010110', '1001011011010111', '1001011011011000', '1001011011011001', '1001011011011010', '1001011011011011', '1001011011011100', '1001011011011101', '1001011011011110', '1001011011011111'], '100101101110', '100101101111'], '10010111', ['100101110001', '100101110010', '100101110011', '100101110100', '100101110101', '100101110110', '100101110111', '100101111000', '100101111001', '100101111010', '100101111011', '100101111100', '100101111101', '100101111110', '100101111111'], '10011000', '10011001', '10011010', ['100110100001', '100110100010', '100110100011', '100110100100', '100110100101', '100110100110', '100110100111', '100110101000', '100110101001', '100110101010', '100110101011', '100110101100', '100110101101', '100110101110', '100110101111'], '10011011', ['100110110001', '100110110010', '100110110011', '100110110100', '100110110101', '100110110110', '100110110111', '100110111000', '100110111001', '100110111010', '100110111011', '100110111100', '100110111101', '100110111110', '100110111111'], '10011100', '10011101', ['100111010001', '100111010010', '100111010011', '100111010100', '100111010101', '100111010110', '100111010111', '100111011000', '100111011001', '100111011010', '100111011011', '100111011100', '100111011101', '100111011110', '100111011111'], '10011110', ['100111100001', '100111100010', '100111100011', '100111100100', '100111100101', '100111100110', '100111100111', '100111101000', '100111101001', '100111101010', '100111101011', '100111101100', '100111101101', ['1001111011010001', '1001111011010010', '1001111011010011', '1001111011010100', '1001111011010101', '1001111011010110', '1001111011010111', '1001111011011000', '1001111011011001', '1001111011011010', '1001111011011011', '1001111011011100', '1001111011011101', '1001111011011110', '1001111011011111'], '100111101110', '100111101111'], '10011111', ['100111110001', '100111110010', '100111110011', '100111110100', '100111110101', '100111110110', '100111110111', '100111111000', '100111111001', '100111111010', '100111111011', '100111111100', '100111111101', '100111111110', '100111111111']], '1010', ['10100001', '10100010', ['101000100001', '101000100010', '101000100011', '101000100100', '101000100101', '101000100110', '101000100111', '101000101000', '101000101001', '101000101010', '101000101011', '101000101100', '101000101101', '101000101110', '101000101111'], '10100011', ['101000110001', '101000110010', '101000110011', '101000110100', '101000110101', '101000110110', ['1010001101100001', '1010001101100010', ['10100011011000100001', '10100011011000100010', '10100011011000100011', '10100011011000100100', '10100011011000100101', '10100011011000100110', '10100011011000100111', '10100011011000101000', '10100011011000101001', '10100011011000101010', '10100011011000101011', '10100011011000101100', '10100011011000101101', '10100011011000101110', '10100011011000101111'], '1010001101100011', '1010001101100100', '1010001101100101', '1010001101100110', '1010001101100111', '1010001101101000', '1010001101101001', '1010001101101010', '1010001101101011', '1010001101101100', '1010001101101101', '1010001101101110', '1010001101101111'], '101000110111', '101000111000', '101000111001', ['1010001110010001', '1010001110010010', '1010001110010011', '1010001110010100', '1010001110010101', '1010001110010110', '1010001110010111', '1010001110011000', '1010001110011001', '1010001110011010', '1010001110011011', '1010001110011100', '1010001110011101', '1010001110011110', '1010001110011111'], '101000111010', '101000111011', '101000111100', '101000111101', '101000111110', '101000111111'], '10100100', ['101001000001', '101001000010', '101001000011', '101001000100', '101001000101', '101001000110', '101001000111', '101001001000', '101001001001', '101001001010', '101001001011', '101001001100', '101001001101', '101001001110', '101001001111'], '10100101', ['101001010001', '101001010010', '101001010011', '101001010100', '101001010101', '101001010110', '101001010111', '101001011000', '101001011001', '101001011010', '101001011011', '101001011100', '101001011101', '101001011110', '101001011111'], '10100110', ['101001100001', '101001100010', ['1010011000100001', '1010011000100010', '1010011000100011', '1010011000100100', '1010011000100101', '1010011000100110', '1010011000100111', '1010011000101000', '1010011000101001', '1010011000101010', '1010011000101011', '1010011000101100', '1010011000101101', '1010011000101110', '1010011000101111'], '101001100011', '101001100100', '101001100101', '101001100110', '101001100111', '101001101000', '101001101001', ['1010011010010001', '1010011010010010', '1010011010010011', '1010011010010100', '1010011010010101', '1010011010010110', '1010011010010111', '1010011010011000', '1010011010011001', '1010011010011010', '1010011010011011', '1010011010011100', '1010011010011101', '1010011010011110', '1010011010011111'], '101001101010', ['1010011010100001', '1010011010100010', '1010011010100011', '1010011010100100', '1010011010100101', '1010011010100110', '1010011010100111', '1010011010101000', '1010011010101001', ['10100110101010010001', '10100110101010010010', '10100110101010010011', '10100110101010010100', '10100110101010010101', '10100110101010010110', '10100110101010010111', '10100110101010011000', '10100110101010011001', '10100110101010011010', ['101001101010100110100001', '101001101010100110100010', '101001101010100110100011', '101001101010100110100100', '101001101010100110100101', '101001101010100110100110', '101001101010100110100111', '101001101010100110101000', '101001101010100110101001', '101001101010100110101010', '101001101010100110101011', '101001101010100110101100', '101001101010100110101101', '101001101010100110101110', '101001101010100110101111'], '10100110101010011011', '10100110101010011100', '10100110101010011101', '10100110101010011110', '10100110101010011111'], '1010011010101010', '1010011010101011', '1010011010101100', '1010011010101101', '1010011010101110', '1010011010101111'], '101001101011', '101001101100', '101001101101', ['1010011011010001', '1010011011010010', '1010011011010011', '1010011011010100', '1010011011010101', ['10100110110101010001', '10100110110101010010', '10100110110101010011', '10100110110101010100', '10100110110101010101', '10100110110101010110', '10100110110101010111', '10100110110101011000', '10100110110101011001', '10100110110101011010', '10100110110101011011', '10100110110101011100', '10100110110101011101', '10100110110101011110', '10100110110101011111'], '1010011011010110', '1010011011010111', '1010011011011000', '1010011011011001', '1010011011011010', ['10100110110110100001', '10100110110110100010', '10100110110110100011', '10100110110110100100', '10100110110110100101', '10100110110110100110', '10100110110110100111', '10100110110110101000', '10100110110110101001', ['101001101101101010010001', '101001101101101010010010', '101001101101101010010011', '101001101101101010010100', '101001101101101010010101', '101001101101101010010110', '101001101101101010010111', '101001101101101010011000', '101001101101101010011001', ['1010011011011010100110010001', '1010011011011010100110010010', '1010011011011010100110010011', '1010011011011010100110010100', '1010011011011010100110010101', '1010011011011010100110010110', '1010011011011010100110010111', '1010011011011010100110011000', '1010011011011010100110011001', '1010011011011010100110011010', '1010011011011010100110011011', '1010011011011010100110011100', '1010011011011010100110011101', '1010011011011010100110011110', '1010011011011010100110011111'], '101001101101101010011010', '101001101101101010011011', '101001101101101010011100', '101001101101101010011101', '101001101101101010011110', '101001101101101010011111'], '10100110110110101010', '10100110110110101011', ['101001101101101010110001', '101001101101101010110010', '101001101101101010110011', '101001101101101010110100', '101001101101101010110101', '101001101101101010110110', '101001101101101010110111', '101001101101101010111000', '101001101101101010111001', '101001101101101010111010', '101001101101101010111011', '101001101101101010111100', '101001101101101010111101', '101001101101101010111110', '101001101101101010111111'], '10100110110110101100', '10100110110110101101', '10100110110110101110', '10100110110110101111'], '1010011011011011', '1010011011011100', '1010011011011101', '1010011011011110', '1010011011011111'], '101001101110', '101001101111'], '10100111', ['101001110001', '101001110010', '101001110011', '101001110100', '101001110101', '101001110110', '101001110111', '101001111000', '101001111001', '101001111010', '101001111011', '101001111100', '101001111101', '101001111110', '101001111111'], '10101000', '10101001', '10101010', ['101010100001', '101010100010', '101010100011', '101010100100', '101010100101', '101010100110', '101010100111', '101010101000', '101010101001', '101010101010', '101010101011', '101010101100', '101010101101', '101010101110', '101010101111'], '10101011', ['101010110001', '101010110010', '101010110011', '101010110100', '101010110101', '101010110110', '101010110111', '101010111000', '101010111001', '101010111010', '101010111011', '101010111100', '101010111101', '101010111110', '101010111111'], '10101100', '10101101', ['101011010001', '101011010010', '101011010011', '101011010100', '101011010101', '101011010110', '101011010111', '101011011000', '101011011001', '101011011010', '101011011011', '101011011100', '101011011101', '101011011110', '101011011111'], '10101110', ['101011100001', '101011100010', '101011100011', '101011100100', '101011100101', '101011100110', '101011100111', '101011101000', '101011101001', '101011101010', '101011101011', '101011101100', '101011101101', '101011101110', '101011101111'], '10101111'], '1011', ['10110001', '10110010', '10110011', '10110100', '10110101', ['101101010001', '101101010010', '101101010011', '101101010100', '101101010101', ['1011010101010001', '1011010101010010', '1011010101010011', '1011010101010100', '1011010101010101', '1011010101010110', '1011010101010111', '1011010101011000', '1011010101011001', '1011010101011010', '1011010101011011', '1011010101011100', '1011010101011101', '1011010101011110', '1011010101011111'], '101101010110', ['1011010101100001', '1011010101100010', '1011010101100011', '1011010101100100', '1011010101100101', ['10110101011001010001', '10110101011001010010', '10110101011001010011', '10110101011001010100', '10110101011001010101', '10110101011001010110', '10110101011001010111', '10110101011001011000', '10110101011001011001', '10110101011001011010', '10110101011001011011', '10110101011001011100', '10110101011001011101', '10110101011001011110', '10110101011001011111'], '1011010101100110', '1011010101100111', '1011010101101000', '1011010101101001', '1011010101101010', '1011010101101011', '1011010101101100', '1011010101101101', '1011010101101110', '1011010101101111'], '101101010111', ['1011010101110001', '1011010101110010', '1011010101110011', '1011010101110100', '1011010101110101', '1011010101110110', '1011010101110111', '1011010101111000', '1011010101111001', '1011010101111010', '1011010101111011', '1011010101111100', '1011010101111101', '1011010101111110', '1011010101111111'], '101101011000', '101101011001', ['1011010110010001', '1011010110010010', '1011010110010011', '1011010110010100', '1011010110010101', '1011010110010110', '1011010110010111', '1011010110011000', '1011010110011001', '1011010110011010', '1011010110011011', '1011010110011100', '1011010110011101', '1011010110011110', '1011010110011111'], '101101011010', '101101011011', ['1011010110110001', '1011010110110010', '1011010110110011', '1011010110110100', '1011010110110101', '1011010110110110', '1011010110110111', '1011010110111000', '1011010110111001', '1011010110111010', '1011010110111011', '1011010110111100', '1011010110111101', '1011010110111110', '1011010110111111'], '101101011100', '101101011101', ['1011010111010001', '1011010111010010', '1011010111010011', '1011010111010100', '1011010111010101', ['10110101110101010001', '10110101110101010010', '10110101110101010011', '10110101110101010100', '10110101110101010101', '10110101110101010110', '10110101110101010111', '10110101110101011000', '10110101110101011001', ['101101011101010110010001', '101101011101010110010010', '101101011101010110010011', '101101011101010110010100', '101101011101010110010101', '101101011101010110010110', '101101011101010110010111', '101101011101010110011000', '101101011101010110011001', '101101011101010110011010', '101101011101010110011011', '101101011101010110011100', '101101011101010110011101', '101101011101010110011110', '101101011101010110011111'], '10110101110101011010', '10110101110101011011', '10110101110101011100', '10110101110101011101', '10110101110101011110', '10110101110101011111'], '1011010111010110', '1011010111010111', '1011010111011000', '1011010111011001', '1011010111011010', ['10110101110110100001', '10110101110110100010', '10110101110110100011', '10110101110110100100', '10110101110110100101', '10110101110110100110', '10110101110110100111', '10110101110110101000', '10110101110110101001', '10110101110110101010', '10110101110110101011', '10110101110110101100', '10110101110110101101', '10110101110110101110', '10110101110110101111'], '1011010111011011', '1011010111011100', '1011010111011101', '1011010111011110', '1011010111011111'], '101101011110', '101101011111'], '10110110', '10110111', ['101101110001', '101101110010', '101101110011', '101101110100', '101101110101', '101101110110', ['1011011101100001', '1011011101100010', '1011011101100011', '1011011101100100', '1011011101100101', '1011011101100110', '1011011101100111', '1011011101101000', '1011011101101001', '1011011101101010', '1011011101101011', '1011011101101100', '1011011101101101', '1011011101101110', '1011011101101111'], '101101110111', '101101111000', '101101111001', '101101111010', '101101111011', '101101111100', '101101111101', '101101111110', '101101111111'], '10111000', '10111001', '10111010', ['101110100001', '101110100010', ['1011101000100001', '1011101000100010', '1011101000100011', '1011101000100100', '1011101000100101', ['10111010001001010001', '10111010001001010010', '10111010001001010011', '10111010001001010100', '10111010001001010101', '10111010001001010110', '10111010001001010111', '10111010001001011000', '10111010001001011001', '10111010001001011010', '10111010001001011011', '10111010001001011100', '10111010001001011101', '10111010001001011110', '10111010001001011111'], '1011101000100110', '1011101000100111', '1011101000101000', '1011101000101001', '1011101000101010', '1011101000101011', '1011101000101100', '1011101000101101', '1011101000101110', '1011101000101111'], '101110100011', ['1011101000110001', '1011101000110010', '1011101000110011', '1011101000110100', '1011101000110101', '1011101000110110', '1011101000110111', '1011101000111000', '1011101000111001', '1011101000111010', '1011101000111011', '1011101000111100', '1011101000111101', '1011101000111110', '1011101000111111'], '101110100100', '101110100101', ['1011101001010001', '1011101001010010', '1011101001010011', '1011101001010100', '1011101001010101', '1011101001010110', ['10111010010101100001', '10111010010101100010', '10111010010101100011', '10111010010101100100', '10111010010101100101', '10111010010101100110', '10111010010101100111', '10111010010101101000', '10111010010101101001', '10111010010101101010', '10111010010101101011', '10111010010101101100', '10111010010101101101', '10111010010101101110', '10111010010101101111'], '1011101001010111', '1011101001011000', '1011101001011001', '1011101001011010', '1011101001011011', '1011101001011100', '1011101001011101', '1011101001011110', '1011101001011111'], '101110100110', '101110100111', '101110101000', '101110101001', '101110101010', ['1011101010100001', '1011101010100010', '1011101010100011', '1011101010100100', '1011101010100101', ['10111010101001010001', '10111010101001010010', '10111010101001010011', '10111010101001010100', '10111010101001010101', '10111010101001010110', '10111010101001010111', '10111010101001011000', '10111010101001011001', '10111010101001011010', '10111010101001011011', '10111010101001011100', '10111010101001011101', '10111010101001011110', '10111010101001011111'], '1011101010100110', '1011101010100111', '1011101010101000', '1011101010101001', '1011101010101010', ['10111010101010100001', '10111010101010100010', '10111010101010100011', '10111010101010100100', '10111010101010100101', '10111010101010100110', '10111010101010100111', '10111010101010101000', '10111010101010101001', '10111010101010101010', '10111010101010101011', '10111010101010101100', '10111010101010101101', '10111010101010101110', '10111010101010101111'], '1011101010101011', ['10111010101010110001', '10111010101010110010', '10111010101010110011', '10111010101010110100', '10111010101010110101', '10111010101010110110', '10111010101010110111', '10111010101010111000', '10111010101010111001', '10111010101010111010', '10111010101010111011', '10111010101010111100', '10111010101010111101', '10111010101010111110', '10111010101010111111'], '1011101010101100', '1011101010101101', ['10111010101011010001', '10111010101011010010', '10111010101011010011', '10111010101011010100', '10111010101011010101', '10111010101011010110', '10111010101011010111', '10111010101011011000', '10111010101011011001', '10111010101011011010', '10111010101011011011', '10111010101011011100', '10111010101011011101', '10111010101011011110', '10111010101011011111'], '1011101010101110', '1011101010101111'], '101110101011', '101110101100', '101110101101', ['1011101011010001', '1011101011010010', ['10111010110100100001', '10111010110100100010', '10111010110100100011', '10111010110100100100', '10111010110100100101', '10111010110100100110', '10111010110100100111', '10111010110100101000', '10111010110100101001', '10111010110100101010', '10111010110100101011', '10111010110100101100', '10111010110100101101', '10111010110100101110', '10111010110100101111'], '1011101011010011', ['10111010110100110001', '10111010110100110010', '10111010110100110011', '10111010110100110100', '10111010110100110101', '10111010110100110110', '10111010110100110111', '10111010110100111000', '10111010110100111001', '10111010110100111010', '10111010110100111011', '10111010110100111100', '10111010110100111101', '10111010110100111110', '10111010110100111111'], '1011101011010100', '1011101011010101', '1011101011010110', ['10111010110101100001', '10111010110101100010', '10111010110101100011', '10111010110101100100', '10111010110101100101', '10111010110101100110', ['101110101101011001100001', '101110101101011001100010', '101110101101011001100011', '101110101101011001100100', '101110101101011001100101', '101110101101011001100110', '101110101101011001100111', '101110101101011001101000', '101110101101011001101001', '101110101101011001101010', '101110101101011001101011', '101110101101011001101100', '101110101101011001101101', '101110101101011001101110', '101110101101011001101111'], '10111010110101100111', '10111010110101101000', '10111010110101101001', '10111010110101101010', '10111010110101101011', '10111010110101101100', '10111010110101101101', '10111010110101101110', '10111010110101101111'], '1011101011010111', '1011101011011000', '1011101011011001', ['10111010110110010001', '10111010110110010010', '10111010110110010011', '10111010110110010100', '10111010110110010101', '10111010110110010110', '10111010110110010111', '10111010110110011000', '10111010110110011001', '10111010110110011010', '10111010110110011011', '10111010110110011100', '10111010110110011101', '10111010110110011110', '10111010110110011111'], '1011101011011010', ['10111010110110100001', '10111010110110100010', '10111010110110100011', '10111010110110100100', '10111010110110100101', '10111010110110100110', '10111010110110100111', '10111010110110101000', '10111010110110101001', '10111010110110101010', '10111010110110101011', '10111010110110101100', '10111010110110101101', '10111010110110101110', '10111010110110101111'], '1011101011011011', ['10111010110110110001', '10111010110110110010', '10111010110110110011', '10111010110110110100', '10111010110110110101', '10111010110110110110', '10111010110110110111', '10111010110110111000', '10111010110110111001', '10111010110110111010', '10111010110110111011', '10111010110110111100', '10111010110110111101', '10111010110110111110', '10111010110110111111'], '1011101011011100', '1011101011011101', ['10111010110111010001', '10111010110111010010', '10111010110111010011', '10111010110111010100', '10111010110111010101', '10111010110111010110', '10111010110111010111', '10111010110111011000', '10111010110111011001', '10111010110111011010', '10111010110111011011', '10111010110111011100', '10111010110111011101', '10111010110111011110', '10111010110111011111'], '1011101011011110', ['10111010110111100001', '10111010110111100010', '10111010110111100011', '10111010110111100100', '10111010110111100101', '10111010110111100110', '10111010110111100111', '10111010110111101000', '10111010110111101001', '10111010110111101010', '10111010110111101011', '10111010110111101100', '10111010110111101101', ['101110101101111011010001', '101110101101111011010010', '101110101101111011010011', '101110101101111011010100', '101110101101111011010101', '101110101101111011010110', '101110101101111011010111', '101110101101111011011000', '101110101101111011011001', '101110101101111011011010', '101110101101111011011011', '101110101101111011011100', '101110101101111011011101', '101110101101111011011110', '101110101101111011011111'], '10111010110111101110', '10111010110111101111'], '1011101011011111'], '101110101110', '101110101111'], '10111011', ['101110110001', '101110110010', '101110110011', '101110110100', '101110110101', '101110110110', '101110110111', '101110111000', '101110111001', ['1011101110010001', '1011101110010010', '1011101110010011', '1011101110010100', '1011101110010101', '1011101110010110', ['10111011100101100001', '10111011100101100010', '10111011100101100011', '10111011100101100100', '10111011100101100101', '10111011100101100110', '10111011100101100111', '10111011100101101000', '10111011100101101001', '10111011100101101010', '10111011100101101011', '10111011100101101100', '10111011100101101101', '10111011100101101110', '10111011100101101111'], '1011101110010111', '1011101110011000', '1011101110011001', ['10111011100110010001', '10111011100110010010', '10111011100110010011', '10111011100110010100', '10111011100110010101', '10111011100110010110', '10111011100110010111', '10111011100110011000', '10111011100110011001', '10111011100110011010', '10111011100110011011', '10111011100110011100', '10111011100110011101', '10111011100110011110', '10111011100110011111'], '1011101110011010', '1011101110011011', '1011101110011100', '1011101110011101', '1011101110011110', '1011101110011111'], '101110111010', '101110111011', ['1011101110110001', '1011101110110010', '1011101110110011', '1011101110110100', '1011101110110101', '1011101110110110', '1011101110110111', '1011101110111000', '1011101110111001', '1011101110111010', '1011101110111011', '1011101110111100', '1011101110111101', '1011101110111110', '1011101110111111'], '101110111100', '101110111101', ['1011101111010001', '1011101111010010', '1011101111010011', '1011101111010100', '1011101111010101', '1011101111010110', '1011101111010111', '1011101111011000', '1011101111011001', '1011101111011010', '1011101111011011', '1011101111011100', '1011101111011101', '1011101111011110', '1011101111011111'], '101110111110', '101110111111'], '10111100', '10111101', ['101111010001', '101111010010', '101111010011', '101111010100', '101111010101', '101111010110', '101111010111', '101111011000', '101111011001', '101111011010', '101111011011', '101111011100', '101111011101', '101111011110', '101111011111'], '10111110', ['101111100001', '101111100010', '101111100011', '101111100100', '101111100101', '101111100110', '101111100111', '101111101000', '101111101001', '101111101010', '101111101011', '101111101100', '101111101101', '101111101110', '101111101111'], '10111111'], '1100', '1101', ['11010001', '11010010', '11010011', '11010100', '11010101', ['110101010001', '110101010010', '110101010011', '110101010100', '110101010101', '110101010110', '110101010111', '110101011000', '110101011001', '110101011010', '110101011011', '110101011100', '110101011101', ['1101010111010001', '1101010111010010', '1101010111010011', '1101010111010100', '1101010111010101', '1101010111010110', '1101010111010111', '1101010111011000', '1101010111011001', '1101010111011010', '1101010111011011', '1101010111011100', '1101010111011101', '1101010111011110', '1101010111011111'], '110101011110', '110101011111'], '11010110', '11010111', '11011000', '11011001', '11011010', ['110110100001', '110110100010', '110110100011', '110110100100', '110110100101', '110110100110', '110110100111', '110110101000', '110110101001', '110110101010', '110110101011', '110110101100', '110110101101', '110110101110', '110110101111'], '11011011', ['110110110001', '110110110010', '110110110011', '110110110100', '110110110101', '110110110110', '110110110111', '110110111000', '110110111001', '110110111010', '110110111011', '110110111100', '110110111101', '110110111110', '110110111111'], '11011100', '11011101', '11011110', '11011111'], '1110', ['11100001', '11100010', '11100011', '11100100', '11100101', ['111001010001', '111001010010', '111001010011', '111001010100', '111001010101', '111001010110', '111001010111', '111001011000', '111001011001', '111001011010', '111001011011', '111001011100', '111001011101', '111001011110', '111001011111'], '11100110', '11100111', '11101000', '11101001', '11101010', '11101011', '11101100', '11101101', '11101110', '11101111'], '1111']
    #print model_tree
    #saveModelTree(model_tree)
'''
MAIN METHOD
'''
logging.basicConfig(filename='logs.txt',level=logging.DEBUG)

linea_counter = 0
#translateFile()
print "START!"
start_time = time()

buffer_0001 = []
buffer_0010 = []
buffer_0011 = []
buffer_0100 = []
buffer_0101 = []
buffer_0110 = []
buffer_0111 = []
buffer_1000 = []
buffer_1001 = []
buffer_1010 = []
buffer_1011 = []
buffer_1100 = []
buffer_1101 = []
buffer_1110 = []
buffer_1111 = []


getStart()
execution_time = time() - start_time
if (execution_time >= 60):
    print "\nTime: ", "%02d" % (execution_time/60), ".", "%02d" % (execution_time%60), " m"
else:
    print "\nTime: ", "%02d" % (execution_time), " s"
    
print "\nFINISH!"