#   Progetto di Informatica Biomedica
#   Gruppo Web-Index
##  Vagnarelli Sara                                          


#Schema funzionale



![schema funzionale](SchemaIO1.png "schema funzionale")









__________________________________________________________________________________________________________________





## OBIETTIVI


### Per tutti i Membri:

*Definizione Formato documento JSON per cluster di punti spazialmente vicini
*Studio algoritmi di partizionamento spaziale (GeoHash/Hilbert, qHull...)


### Lavoro individuale  
 
*Ottimizzazione codice, server Python 


____________________________________________________________________________________________________________________





## REALIZZAZIONE



* ottimizzazione codice per la rappresentazione dei punti 3D ricevuti in input.



* implementazione server web in Python

  /localhost:8080/webIndex/query?x=0.5&y=0.7/
   Es.
   input:   prende un modello, coordinate dei punti n-dimensioni
   output:  idCluster


_______________________________________________________________________________________________________________________




## REQUISITI   

* studio database mongoDB
* studio gestione file json 
* programmazione Python




1. **OTTIMIZZAZIONE DEL CODICE**

**prima ottimizzazione "cleaner.py"**

    from time import time
    WIDTH = 800
    HEIGHT = 800
    DEPTH = 1024
    SOURCE = 'bone0.txt'
    DESTINATION = 'bone_clean.txt'
    points_counter = 0

    def clean(down, middle, up):
     global points_counter
     middle_clean = []
     middle_clean.append(middle[0])
    
     for x in range(WIDTH):
        if (middle[0][x] == '1'):
                points_counter += 1
    
     for y in range(1, HEIGHT-1):
        row = []
        row.append(middle[y][0])        
        if (row[0] == '1'):
                points_counter += 1
        
        for x in range(1, WIDTH-1):
            if (middle[y][x] == '1'):
                if (middle[y-1][x] == '1' and
                    middle[y+1][x] == '1' and
                    middle[y][x-1] == '1' and
                    middle[y][x+1] == '1' and
                    up[y][x] == '1' and
                    down[y][x] == '1'):
                    row.append('0')
                else:
                    row.append('1')
            else:
                row.append('0')                
            if (row[x] == '1'):
                points_counter += 1
                
        row.append(middle[y][WIDTH-1])
        if (row[WIDTH-1] == '1'):
                points_counter += 1
                
        middle_clean.append(row)
        
     middle_clean.append(middle[HEIGHT-1])
     for x in range(WIDTH):
         if (middle[HEIGHT-1][x] == '1'):
                 points_counter += 1
                
     return middle_clean

    def loadSlice(input):
     slice = []
     input.readline()
     for y in range(HEIGHT):
        slice.append(input.readline())
     return slice


'''dice quale slice stai guardando..devo saltare ilcommento nella lettura'''
  
    def writeSlice(output, slice, id):
     output.write('# New slice (' + str(id) + ')\n')
     for y in range(HEIGHT):
        row = ""
        for x in range(WIDTH):
            row += slice[y][x]
        output.write(row + '\n')

    def addPoints(slice):
     global points_counter
     for row in slice:
        for x in row:
            if (x == '1'):
                points_counter += 1

    print "START!"
    start_time = time()

    input = open(SOURCE, 'r')
    output = open(DESTINATION, 'w')


'''divido il cubo in slice e ne prendo tre per volta, quella sopra e l'ultima le devo tenere.'''




    down = loadSlice(input)
    middle = loadSlice(input)
    up = loadSlice(input)
    writeSlice(output, down, 0)
    '''quanti punti ho in una slice'''
    addPoints(down)
    print "clean 0"
    '''cancella i punti inerni nella middle

    '''scrive solo middle'''
    writeSlice(output, clean(down, middle, up), 1)
    print "clean 1"

    '''carico le nuove slice'''
    for z in range(2, DEPTH-1):
     down = middle
     middle = up
     up = loadSlice(input)
     writeSlice(output, clean(down, middle, up), z)
     print "clean", z

    
    
'''sono arrivata all'ultima prendi up che nn devi ottimizzare e la scrivi
    
    
    
    
    writeSlice(output, up, DEPTH-1)
    addPoints(up)
    print "clean 1023"

    input.close()
    output.close()

    print "number of points:", points_counter

    execution_time = time() - start_time
    if (execution_time >= 3600):
      print "\nTime: ", "%02d" % (execution_time/3600), ".", "%02d" % ((execution_time%3600)/60), " h"
    elif (execution_time >= 60):
     print "\nTime: ", "%02d" % (execution_time/60), ".", "%02d" % (execution_time%60), " m"
    else:
     print "\nTime: ", "%02d" % (execution_time), " s"
    print "FINISH!"
    
    
***
