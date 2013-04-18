# Progetto Informatica Biomedica (Web-Index)
# Andrea Patrizio

## Progettazione ed implementazione di un Partizionatore Classico 

![schema funzionale](SchemaWebIndex.png "schema funzionale")

## Problemi da affrontare

* A partire da un grosso modello, partizionarlo in cluster di punti
* Salvataggio dei cluster su MongoDB attraverso file JSON
* Definizione di una funzione di retrieve

## Utilizzo di tecniche Geohash

### Partizionamento 2D
![geohash](geohash.png "geohash")

### Albero delle partizioni
![quadtree](quadtree.png "quadtree")

### Retrieve dei dati
![geohash-query](geohash-query.png "geohash-query")

## Utilizzo delle curve di Hilbert

### Sviluppo della curva in 2D
![hilbert_curve](hilbert_curve.png "hilbert_curve")

### Sviluppo della curva in 3D
![hilbert3d-o1](hilbert3d-o1.png "hilbert3d-o1")
![hilbert3d-o2](hilbert3d-o2.png "hilbert3d-o2")