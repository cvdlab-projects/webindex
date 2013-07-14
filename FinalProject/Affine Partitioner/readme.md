#Web Index
##Affine Coordinates partitioner
![Schema](https://raw.github.com/cvdlab-bio/webindex/patrizio_dev_branch/FinalProject/SchemaWebIndex.png)

##Tasks:
Create a partioner for a 3D model. 
The partitioner must divide the model in clusters of points using affine coordinates system.
The clusters are saved on MongoDB.

Problems:
* High computational complexity of the algorithm.
* Preserve the memory. Integration of a buffering system.



##The partitioner
Precondition:
* this partitioner needs a set of points in 4D. Before you start the partitioner is necessary to bring all the points from 3D to 4D by adding a dimension with value 1, then rewrite the file.

Input:
* A file with rows of 10000 4D points
* The threshold for the clusters
* Some attributes of the model (name, description, dimensions)

Output:
* Clusters of points saved on MongoDB
* The model-three of the partition (see Ilario Maiolo's [page](https://github.com/cvdlab-bio/webindex/blob/maiolo_dev_branch/Maiolo/2013-04-18/maiolo.md))


This algorithm can not be represented graphically because it works in 4D space.

The partitioner uses a pseudo recursive algorithm.
Basicly it is a recursive algorithm, but with some tricks to preserve the memory load.
It uses some global buffer. One for any cluster and it makes sure to empty it (write points in files) before moving on to the next depth level.

For each depth level, the partitioner choose 4 points from the cluster an generate a Trasformation Matrix with it.





![getStart](https://raw.github.com/cvdlab-bio/webindex/pisanu_dev_branch/FinalProject/Affine%20Partitioner/getStart.png)
![processFile](https://raw.github.com/cvdlab-bio/webindex/pisanu_dev_branch/FinalProject/Affine%20Partitioner/processFile.png)
![processChunk](https://raw.github.com/cvdlab-bio/webindex/pisanu_dev_branch/FinalProject/Affine%20Partitioner/processChunk.png)


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
* The model-tree is created at the beginning of the algorithm and updated at the cluster creation
* The clusters are saved in group on MongoDB (for efficiency)
