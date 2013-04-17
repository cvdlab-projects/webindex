#Web Index
##Viewer of a tree that represents the decomposition of an image.


###Ilario Maiolo
###Informatica Biomedica
####2012/2013

- - -

![ScreenShot](https://raw.github.com/cvdlab-bio/webindex/maiolo_dev_branch/slides%20Ilario%20Maiolo/immagine_sommario.png)

- - -

#Problem:
###Use a representation that permit an easier debug understanding for the partitioning algorithm

- - -

#Solution:

![ScreenShot](https://raw.github.com/cvdlab-bio/webindex/maiolo_dev_branch/slides%20Ilario%20Maiolo/image_final.png)	

###1,2,3... in the image above represent the CLUSTER_ID.

##First Step:
	1)Create a function to retrieve a json document using MongoDb.
	2)For each cluster find the number of vertices. 

##Second Step:
	1)Create a tree representation of an image using javascript.
	2)Display the number of vertices on the tree
- - -