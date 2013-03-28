% Progetto Informatica Biomedica
% WebIndex
% Marzo 2013

# Web Spatial Index project

## Obiettivi

- Analysis of major approaches to spatial indexing of large point data-sets
- JSON paging of large geometric datasets using MongoDB
- implementation of Hilbert Lebesgue curve and indices

## Autori

Andrea Barbadoro, Andrea Patrizio, Claudio Pisanu, Francesco Maglia, Ilario Maiolo, Matteo Cannaviccio, Sara Vagnarelli

# Schema Funzionale
\includegraphics[keepaspectratio,width=\textwidth, height=.8\textheight]{SchemaFunzionale.jpg} 

# Task

## Comuni:

- Definizione Formato documento JSON per cluster di punti spazialmente vicini
- Studio algoritmi di partizionamento spaziale (GeoHash/Hilbert, qHull...)

## Indipendenti:
- Partizionatore per Coordinate Affini
    - Andrea Barbadoro, Claudio Pisanu, Ilario Maiolo
- Partizionatore Classico
    - Andrea Patrizio, Francesco Maglia
- Libreria recupero documenti
    - Matteo Cannaviccio, Sara Vagnarelli
