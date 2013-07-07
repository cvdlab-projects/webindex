#Web Index
##Classic partitioner
![Schema](https://raw.github.com/cvdlab-bio/webindex/patrizio_dev_branch/FinalProject/SchemaWebIndex.png)

##Tasks:
Create a partioner for a 3D model. 
The partitioner must divide the model in clusters of points.
The clusters are saved on MongoDB.

Big problems:
* Extract points from a set of png images (that represent the 3D model)
* Run the partitioner on this set of points

##First task: Extract points
Precondition:
* The model is represented by a set of images (with extension .png)
* The images are in a sequence order (e.g. from "slice0.png" to "slice100.png")

Input:
* Number of images
* Source directory (in which the images are saved)
* Destination file
* One image for the kmeans algorithm

Output:


A file that represent the points of the model.
This file has, for all the slice (or image) of the model, a binary matrix.
If the model has N images than the file has N matrix.
For the z-matrix there is a 1 in the y-row at the position x, only if there is a point in the coordinate (x,y,z) in the model.
Each slice is separeted by a comment.

The following image explane the process of the algorithm:
![Model2slices](https://raw.github.com/cvdlab-bio/webindex/patrizio_dev_branch/FinalProject/Model2slices.png)

High level algorithm:
	Generate the centroid (background, foreground) for the model
	For each image:
		load the png image
		make a quantization of the points (using the centroid)
		save the slice in the output file

Python algorithm:
    from time import time
    from scipy import *
    import numpy as np
    from numpy import reshape,array
    from scipy.cluster.vq import kmeans,vq
    import png
    from scipy import ndimage
    
    # -------------------------------------------
    # VARIABLES AND CONSTANTS
    # -------------------------------------------
    
    #number of slices for a file
    DEPTH = 1024
    #number of colors for the kmeans
    COLORS = 2
    #source for input (only the prefix)
    SOURCE = 'bone/bone.'
    #source (the slice) for the kmeans png 
    KMEANS = 244
    #destination for the output
    DESTINATION = 'bone'
    #to count the points in the model
    points_counter = 0
    
    # -------------------------------------------
    # METHODS
    # -------------------------------------------
    
    #read a png given his id
    def readPng(id):
        print "reading png", id
        filename = SOURCE + str(id) + '.png'
        reader = png.Reader(filename)
        content = reader.read()
        page = [list(row) for k,row in enumerate(content[2])]
        return array(page, dtype='uint8')
    
    #returns the centroids for the model
    def getCentroids():
        png = readPng(KMEANS)
        pixel = reshape(png, (png.shape[0] * png.shape[1], 1))
        centroids, _ = kmeans(pixel, COLORS)
        if centroids[0] > centroids[1]:
            centroids = array([centroids[1], centroids[0]], dtype='uint8')
        print "centroids: background =", centroids[0], ", foreground =", centroids[1]
        return centroids
    
    #returns the slice of the given png
    def getSlice(png, centroids):
        print "get slice"
        png = ndimage.median_filter(png, 10)
        pixel = reshape(png, (png.shape[0] * png.shape[1], 1))
        qnt, _ = vq(pixel, centroids)
        slice = reshape(qnt, png.shape)
        return array(slice, dtype='string')
    
    #add the points of the array in point_counter
    def addPoints(slice):
        global points_counter
        for row in slice:
            for value in row:
                if value == '1':
                    points_counter += 1
    
    #saves the slice on disk
    def saveSlice(outfile, slice, id):
        print "save slice"
        outfile.write('# New slice (' + str(id) + ')\n')
        np.savetxt(outfile, slice, delimiter='', fmt='%-c')
    
    #saves a set of slices on disk
    def png2array(centroids):     
        outfile = file(DESTINATION + '.txt', 'w')
    
        for id in range(DEPTH):
            png = readPng(id)
            slice = getSlice(png, centroids)
            addPoints(slice)
            saveSlice(outfile, slice, id)        
        
        outfile.close()
        
    # -------------------------------------------
    # MAIN METHOD
    # -------------------------------------------
    
    print "START!"
    start_time = time()
    
    centroids = getCentroids()
    png2array(centroids)    
    print "number of points: ", points_counter
    
    execution_time = time() - start_time
    if execution_time >= 3600:
        print "\nTime: ", "%02d" % (execution_time/3600), ".", "%02d" % ((execution_time%3600)/60), " h"
    elif (execution_time >= 60):
        print "\nTime: ", "%02d" % (execution_time/60), ".", "%02d" % (execution_time%60), " m"
    else:
        print "\nTime: ", "%02d" % (execution_time), " s"
        
    print "\nFINISH!"

##Second task: The partitioner
Precondition:
* After the extraction, the points of the model are saved in a file and re-writed for optimization (see Sara Vagnarelli's page).
* A row of a slice represents only the x-coordinate of a point

Input:
* The file in which the slices are saved
* The threshold for the clusters
* Some attributes of the model (name, description, dimensions)

Output:
* Clusters of points saved on MongoDB
* The model-three of the partition
* Some information as clusters created and the biggest/smaller cluster

The following image explane the process of the algorithm:
![Partitioner](https://raw.github.com/cvdlab-bio/webindex/patrizio_dev_branch/FinalProject/Partitioner.png)

High level algorithm:
	Calculate the minimum set of clusters (dipending on memory usage)

 
 
