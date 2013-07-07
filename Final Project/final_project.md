#Web Index
##Classic partitioner
![Schema](https://raw.github.com/cvdlab-bio/webindex/patrizio_dev_branch/FinalProject/SchemaWebIndex.png)

#Tasks:
Create a partioner for a 3D model. 
The partitioner must divide the model in clusters of points.
The clusters are saved on MongoDB.

Big problems:
* Extract points from a set of png images (that represent the 3D model)
* Run the partitioner on this set of points

#First task: Extract points
Precondition:
* The model is represented by a set of images (with extention .png)
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

The following image explane the process of the algorithm.
![Model2slices](https://raw.github.com/cvdlab-bio/webindex/patrizio_dev_branch/FinalProject/Model2slices.png)

High level algorithm:
	Generate the centroid (background, foreground) for the model
	For each image:
		load the png image
		make a quantization of the points
		save the slice in the output file