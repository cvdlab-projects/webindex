#Web Index
##Viewer of a tree that represents the decomposition of an image.


###Ilario Maiolo
###Informatica Biomedica
####2012/2013

- - -

![ScreenShot](https://raw.github.com/cvdlab-bio/webindex/maiolo_dev_branch/Maiolo/2013-04-18/immagine_sommario.png)

- - -

#Problem:
###Use a representation that permit an easier debug understanding for the partitioning algorithm

- - -

#Solution:

![ScreenShot](https://raw.github.com/cvdlab-bio/webindex/maiolo_dev_branch/Maiolo/2013-04-18/image_final.png)	

###1,2,3... in the image above represent the CLUSTER_ID.
---
##First Step:
	1)Create a function to retrieve a json document using MongoDb.
	 

##Second Step:
	1)Create a tree representation of an image using javascript.
	2)Display the CLUSTER_ID on the tree
	
- - -
#Solution First Step:

	1)Create a function to retrieve a json document using MongoDb.
	
	For the first point I developed a function that through an ajax request at mongodb rest interface recovers the json document (the document describes the model partitioned)	

---	
##Function:
	
	$(function () {
        function retriveJsonDocument() {
		clearDivResult(); //this function cleans the div that contains the image of the tree
		var value = document.getElementById('inputModelId').value;
         $.ajax({ 
             url:'http://localhost:28017/ilariomaiolodb/documents/?filter_id=modello'+value,
             type: 'get',
             dataType: 'jsonp',
             jsonp: 'jsonp', // mongod is expecting the parameter name to be called "jsonp"
             success: function (data) {
				 //if the document doesn't exist launch an alert
                 if (typeof (data["rows"][0]) === "undefined") {
                     alert("doesn't exist a model with id : " + value)
                 } else {
                    //Retrive clusters_tree 
                     var clustersTree = data["rows"][0]["clusters_tree"];
              
					 //Print the info of the cluster
                     var type = data["rows"][0]["type"];
                     var description = data["rows"][0]["description"];
                     var id = data["rows"][0]["id"];
                     var name = data["rows"][0]["name"];

                    //function that print the tree
                     createTree(clustersTree, type, description, id, name);
                 }
             },
             
			 error: function (XMLHttpRequest, textStatus, errorThrown) {
                 console.log('error', errorThrown);
             }
         });
     }); 
    }

---

#Solution Second Step:
	
	1)Create a tree representation of an image using javascript.
	
	For the creation of the tree i have chosen the raphaeljs library and i have developed a recursive algorith to iterate each node after the partion


---

##Function:
	function createTree(clusterTree, type, description, id, name) {
		//Space in which i want to draw 
		var divResult = document.getElementById('printResult');
		space2Draw = new Raphael(divResult, 200000, 200000);

		//Print the root 
		var coordinatesRoot = printRoot(space2Draw);

		//coordinates of the circle
		var xNewCord = coordinatesRoot[0];
		var yNewCord = coordinatesRoot[1]

		//coordinates for the arches
		var xOldCord = coordinatesRoot[0];
		var yOldCord = coordinatesRoot[1];

		//Print the description     
        space2Draw.text(100, 25, "Type: " + type);
        space2Draw.text(100, 45, "Id: " + id);
        space2Draw.text(100, 65, "Name: " + name);
        space2Draw.text(100, 85, "Description: " + description);
        
        var haFigli = false;
        var isUltimo = false; 

        for (var i = 0; i < clusterTree.length;i++){  
            if (typeof (clusterTree[i]) === "string") {
                if (i === (clusterTree.length - 1)) {
                    xNewCord += 150;
                }
					var coordElement = printElement(clusterTree[i], xNewCord, yNewCord, xOldCord, yOldCord, space2Draw, type, id, name, description, haFigli,isUltimo);
					xNewCord = coordElement[0];
					yNewCord = coordElement[1];
					xOldCord = coordElement[2];

            } else {
                 var coord = printUnderTree(clusterTree[i], xNewCord, yNewCord, xOldCord, yOldCord, space2Draw, type, id, name, description, haFigli, isUltimo);
                 xNewCord = coord;
              }
        
        }


	}



---

	2)Display the CLUSTER_ID on the tree

	In this step i have developed some function that show the CLUSTER ID using a jquery plugin "SimpleTip"

---
##Function:
	function addTip(node, tip) {
		$(node).mouseenter(function () {
			tip.fadeIn();
			over = true;
    }).mouseleave(function () {
        tip.fadeOut(10);
        over = false;
		});
    }
    
	function convertValue(value,from,to) {
		if (typeof(from)==="undefined" && typeof (to)=== "undefined") {
			var valueLength = value.length;
			return value.substring(valueLength - 3, valueLength);
		}
			else{

			var valueLength = value.length;
			return value.substring(valueLength - from, valueLength-to);

			}
		}
