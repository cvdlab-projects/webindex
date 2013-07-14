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


below we can find the flow diagrams of some of the most important methods of the partitioner.

#getStart()
![getStart](https://raw.github.com/cvdlab-bio/webindex/pisanu_dev_branch/FinalProject/Affine%20Partitioner/getStart.png)

#processFile(...)
![processFile](https://raw.github.com/cvdlab-bio/webindex/pisanu_dev_branch/FinalProject/Affine%20Partitioner/processFile.png)

processChunk(...)
![processChunk](https://raw.github.com/cvdlab-bio/webindex/pisanu_dev_branch/FinalProject/Affine%20Partitioner/processChunk.png)




Notes:
* The model-tree is created at the beginning of the algorithm and updated at the cluster creation

