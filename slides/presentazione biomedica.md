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
 
*Libreria recupero dei cluster, server Python 


____________________________________________________________________________________________________________________





## REALIZZAZIONE



* implementazione metodi per il recupero del Cluster....

  ES. int getID(int i, intj....)
  input: coordinate spaziali punto...
  output: idcluster

  ###gestione coordinate n-dimensioni



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
