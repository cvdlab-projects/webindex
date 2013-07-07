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
* One image for generate the centroid (background, foreground)

Output:

A file that represent the points of the model.
This file has, for each slice (or image) of the model, a binary matrix.
If the model has N images than the file has N matrixes.
For the z-matrix there is a 1 in the y-row at the position x, only if there is a point in the coordinate (x,y,z) in the model.
Each slice is separeted by a comment.

The following image explane the process of the algorithm:
![Model2slices](https://raw.github.com/cvdlab-bio/webindex/patrizio_dev_branch/FinalProject/Model2slices.png)

High level algorithm:

    Generate the centroid for the model
    For each image:
        Load the png image
        Make a quantization of the points (using the centroid)
        Save the slice in the output file

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

Notes:
* The centroid is generated using the [kmeans algorithm](http://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans.html#scipy.cluster.vq.kmeans)
* For each slice is applied a [median filter](http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.filters.median_filter.html) and a [quantization](http://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.vq.html#scipy.cluster.vq.vq)

##Second task: The partitioner
Precondition:
* After the extraction, the points of the model are saved in a file and re-writed for optimization (see Sara Vagnarelli's [page](https://github.com/cvdlab-bio/webindex/blob/vagnarelli_dev_branch/README.md)).
* A row of a slice represents only the x-coordinate of a point

Input:
* The file in which the slices are saved
* The threshold for the clusters
* Some attributes of the model (name, description, dimensions)

Output:
* Clusters of points saved on MongoDB
* The model-three of the partition (for visualization, see Ilario Maiolo's [page](https://github.com/cvdlab-bio/webindex/blob/maiolo_dev_branch/Maiolo/2013-04-18/maiolo.md))
* Some information as clusters created and the biggest/smaller cluster

The following image explane the process of the algorithm:
![Partitioner](https://raw.github.com/cvdlab-bio/webindex/patrizio_dev_branch/FinalProject/Partitioner.png)

High level algorithm:

    Calculate the minimum set of clusters (depending on memory usage)
    For each clusters:
        Load the cluster in memory
        Divide the cluster in sub-clusters (depending on the threshold)
        Save the clusters on MongoDB

Python algorithm:

    from time import time
    from pymongo import MongoClient
    import types
    import json
    import math
    
    # -------------------------------------------
    # VARIABLES AND CONSTANTS
    # -------------------------------------------
    
    #source for input
    SOURCE = 'bone_op'
    #threshold of the number of points in a single cluster
    POINT_THRESHOLD = 50000
    #name of the model
    NAME = "osso spugnoso"
    #description of the model
    DESCRIPTION = "il modello di un osso spugnoso"
    #dimensions of the model 
    WIDTH = 800
    HEIGHT = 800
    DEPTH = 1024
    #dimensions of the clusters
    CLUSTER_WIDTH = WIDTH
    CLUSTER_HEIGHT = HEIGHT
    CLUSTER_DEPTH = DEPTH
    #maximum memory for a cluster
    MAX_MEM = 400 * 400 * 512
    #tree of the cluster
    MODEL_TREE = ["000", "001", "010", "100", "011", "101", "110", "111"]
    #array of documents to insert on mongodb
    DOCS = []
    #number of documents of a insert request to mongodb
    DOCS_THRESHOLD = 10 * 250000 / POINT_THRESHOLD
    #to calculate min/max/avg cluster
    max_points = 0
    max_cluster = None
    min_points = POINT_THRESHOLD
    min_cluster = None
    tot_points = 0
    
    # -------------------------------------------
    # CREATES CONNECTION TO MONGODB
    # -------------------------------------------
    
    #make a connection with mongodb and get the collection 'clusters'
    print "connecting to mongodb..."
    client = MongoClient('localhost', 27017)
    db = client['db-bio']
    db.drop_collection('clusters')
    CLUSTERS = db.clusters
    print "connection success"
    
    # -------------------------------------------
    # DEFINES CLUSTER CLASS
    # -------------------------------------------
    
    #class that represents a cluster
    #a cluster has
    #  id: a unique string of 0 and 1
    #  location: coordinates (x, y, z) in the world
    #  dimension: width, height, depth of the cluster
    #  slices: array 3D of the points of the cluster
    #  points: number of points of the cluster
    class Cluster:
        def __init__(self, id):
            self.id = id
        def setLocation(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z
        def setDimension(self, w, h, d):
            self.width = w
            self.height = h
            self.depth = d
        def setSlices(self, slices):
            self.slices = slices
            self.points = 0
            for slice in slices:
                for row in slice:
                    self.points += len(row)
            
    # -------------------------------------------
    # METHODS
    # -------------------------------------------
    
    #print a Cluster
    def printCluster(cluster):
        print "  - cluster info -"
        print "    id :", cluster.id
        print "    location :", cluster.x, cluster.y, cluster.z
        print "    dimension :", cluster.width, cluster.height, cluster.depth   
        print "    points :", cluster.points, "\n"
    
    #add a cluster to the model tree
    def addToModelTree(array, cluster, new_clusters):
        for index, elem in enumerate(array):
            if isinstance(elem, types.StringType):
                if cluster.id == elem:
                    clusters_id = []
                    for c in new_clusters:
                        clusters_id.append(c.id)
                    array[index] = clusters_id
                    return True
            else:
                if addToModelTree(elem, cluster, new_clusters):
                    return True
        return False
    
    #save the model tree in mongodb
    def saveModelTree():
        print "...to disk"
        print "saving model_tree..."    
        post = {}
        post["_id"] = "model"
        post["name"] = NAME
        post["description"] = DESCRIPTION
        post["dimensions"] = [WIDTH, HEIGHT, DEPTH]
        post["clusters_tree"] = MODEL_TREE
        CLUSTERS.insert(post)
        if (len(DOCS) > 0):   
            CLUSTERS.insert(DOCS)
    
    #save a cluster in mongodb
    def saveCluster(cluster):
        print "saving..."    
        post = {}
        post["_id"] = cluster.id
        post["location"] = (cluster.x, cluster.y, cluster.z)
        post["dimension"] = (cluster.width, cluster.height, cluster.depth)
        
        json_slices = []
        for slice in cluster.slices:
            json_slice = []
            for y, row in enumerate(slice):
                for x in row:
                    json_slice.append([int(x), y])
            json_slices.append(json_slice)    
        post["points"] = json_slices
        
        DOCS.append(post)
        if len(DOCS) == DOCS_THRESHOLD:
            print "...to disk"
            CLUSTERS.insert(DOCS)
            del DOCS[:]
    
    #verify that a cluster have the right number of points
    def verifyCluster(cluster):
        print "verify"    
        if cluster.points >= POINT_THRESHOLD:
            return False
        
        global max_points
        global max_cluster
        global min_points
        global min_cluster
        global tot_points
        
        if cluster.points > max_points:
            max_points = cluster.points
            max_cluster = cluster        
        if cluster.points < min_points:
            min_points = cluster.points
            min_cluster = cluster        
        tot_points += cluster.points
        
        return True
    
    #load a slice from the given file
    #x and y are used to 'cut' the slice
    def loadSlice(in_file, x, y):
        slice = []
        in_file.readline() #jump over the comment '#New slice'
        
        for i in range(y):
            in_file.readline()
        
        for i in range(CLUSTER_HEIGHT):
            row = []
            for v in in_file.readline().split():
                if int(v) >= x and int(v) < x + CLUSTER_WIDTH:
                    row.append(v)
            slice.append(row)
                
        for i in range(HEIGHT - CLUSTER_HEIGHT - y):
            in_file.readline()
                
        return slice
    
    #load a set of slice from the given file
    #x, y, z are used to 'cut' the slices
    def loadSlices(in_file, x, y, z):    
        for i in range(z):
            in_file.readline() #jump over the comment '#New slice'
            for j in range(HEIGHT):
                in_file.readline()
                
        slices = []
        for i in range(CLUSTER_DEPTH):
            slice = loadSlice(in_file, x, y)
            slices.append(slice)    
        return slices
    
    #load a cluster given his id
    def loadCluster(id):
        print "loading cluster..."
        
        x = 0
        y = 0
        z = 0
        ancestors = len(id) / 3
        f = int(math.pow(2, ancestors - 1))
        for i in range(ancestors):
            x += int(id[i * 3]) * CLUSTER_WIDTH * f
            y += int(id[i * 3 + 1]) * CLUSTER_HEIGHT * f
            z += int(id[i * 3 + 2]) * CLUSTER_DEPTH * f
            f /= 2
        
        in_file = open(SOURCE + '.txt', 'r')
        slices = loadSlices(in_file, x, y, z)
        in_file.close()
            
        cluster = Cluster(id)
        cluster.setLocation(x, y, z)
        cluster.setDimension(CLUSTER_WIDTH, CLUSTER_HEIGHT, CLUSTER_DEPTH)
        cluster.setSlices(slices)    
        return cluster
    
    #given a cluster, returns the sub-cluster with the given 'code coordinates'
    def subCluster(cluster, x, y, z):
        width = cluster.width / 2
        height = cluster.height / 2
        depth = cluster.depth / 2
        
        if z == 0:
            sub_slices = cluster.slices[:depth]
        else:
            sub_slices = cluster.slices[depth:]
        
        for d in range(depth):
            if y == 0:
                sub_slices[d] = sub_slices[d][:height]
            else:
                sub_slices[d] = sub_slices[d][height:]
        
        for d in range(depth):
            for h in range(height):
                row = []
                for v in sub_slices[d][h]:
                    if x == 0:
                        if int(v) < cluster.x + width:
                            row.append(v)
                    else:
                        if int(v) >= cluster.x + width:
                            row.append(v)
                sub_slices[d][h] = row
                            
        sub_cluster = Cluster(cluster.id + str(x) + str(y) + str(z))
        sub_cluster.setLocation(cluster.x + width * x, cluster.y + height * y, cluster.z + depth * z)
        sub_cluster.setDimension(width, height, depth)
        sub_cluster.setSlices(sub_slices) 
        print "  created cluster"
        printCluster(sub_cluster)    
        return sub_cluster
    
    #divide the given cluster to obtain 8 new cluster
    def divideCluster(cluster):
        print "divide"
        clusters = []    
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    clusters.append(subCluster(cluster, x, y, z))                
        addToModelTree(MODEL_TREE, cluster, clusters)    
        return clusters
    
    #create the partition for the cluster with the given id
    def partitioningCluster(id):
        print "partitioning cluster", id
        clusters = []
        clusters.append(loadCluster(id))
        
        while len(clusters) > 0:
            cluster = clusters[0]
            print "chosen cluster"
            printCluster(cluster)
            if verifyCluster(cluster):
                saveCluster(cluster)
            else:
                clusters += divideCluster(cluster)
            del clusters[0]
        
    # -------------------------------------------
    # MAIN METHOD
    # -------------------------------------------       
    
    print "START!"
    start_time = time()
    
    print "generate primary clusters"
    if CLUSTER_WIDTH * CLUSTER_HEIGHT * CLUSTER_DEPTH <= MAX_MEM:
        print "only one step!"
        partitioningCluster("000")
        MODEL_TREE = ["000"]
    else:
        partitioning = 0    
        while CLUSTER_WIDTH * CLUSTER_HEIGHT * CLUSTER_DEPTH > MAX_MEM:
            CLUSTER_WIDTH /= 2
            CLUSTER_HEIGHT /=2
            CLUSTER_DEPTH /= 2
            partitioning += 1
            
        clusters = [""]
        for p in range(partitioning):
            new_clusters = []
            for x in range(2):
                for y in range(2):
                    for z in range(2):
                        for c in clusters:
                            new_clusters.append(c + str(x) + str(y) + str(z))
            del clusters[:]
            clusters += new_clusters
        
        for c in clusters:
            partitioningCluster(c)
    saveModelTree()
        
    print "\nFINISH!"
    execution_time = time() - start_time
    if execution_time >= 60:
        print "Time: ", "%02d" % (execution_time/60), ".", "%02d" % (execution_time%60), " m"
    else:
        print "Time: ", "%02d" % (execution_time), " s"
    
    print "\nSTATISTICS:"
    docs = CLUSTERS.count()
    print "documents created: ", docs
    print "total points:", tot_points
    print "biggest cluster:", max_cluster.id, "with", max_points, "points"
    print "smaller cluster:", min_cluster.id, "with", min_points, "points"
    print "avg points per cluster:", tot_points/(docs-1) #-1: the tree of the model

Notes:
* The model-tree is created at the beginning of the algorithm and updates at cluster creation
* The cluster are saved in group on MongoDB (for efficiency)
