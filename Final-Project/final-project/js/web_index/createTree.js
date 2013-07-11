

function createTree(clustersTree, dimension, description, id, name) {
    console.log(clustersTree+"  cda");
    //Nascondo gli input
    //document.getElementById('inputModelId').value = " ";

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
        space2Draw.text(100, 25, "Dimension: " + dimension);
        space2Draw.text(100, 45, "Id: " + id);
        space2Draw.text(100, 65, "Name: " + name);
        space2Draw.text(100, 85, "Description: " + description);
        
        var haFigli = false;
        var isUltimo = false; 

        for (var i = 0; i < clustersTree.length; i++) {
           
            if (typeof (clustersTree[i]) === "string") {
                if (i === (clustersTree.length - 1)) {
                    xNewCord += 150;
                }
                var coordElement = printElement(clustersTree[i], xNewCord, yNewCord, xOldCord, yOldCord, space2Draw, haFigli, isUltimo);
                xNewCord = coordElement[0];
                yNewCord = coordElement[1];
                xOldCord = coordElement[2];

            } else {
                
                var coord = printUnderTree(clustersTree[i], xNewCord, yNewCord, xOldCord, yOldCord, space2Draw, haFigli, isUltimo);
                 xNewCord = coord;
              }
        
        }


}

var over = false;
function printElement(clusterTree, xNewCord, yNewCord, xOldCord, yOldCord, space2Draw, haFigli,isUltimo) {
    //Mi sposto a sx dal padre che mi ha chiamato (deve essere uguale tra le due funzioni)
    var newXCoordinates = xNewCord - 80;
    var newYCoordinates = yNewCord + 80;


    st = space2Draw.set();
    var a;
            st.push(
                 a = space2Draw.circle(newXCoordinates, newYCoordinates, 15).click((function (clusterTree) {
                     return function () {
                         window.open("index-point.html?id=" + (clusterTree));
                     }
                 }(clusterTree))).mouseover(function () {
                     this.attr({ 'cursor': 'pointer' });
                     this.attr({ 'opacity': '.50' });
                 }).mouseout(function () {
                     this.attr({ 'opacity': '1' });
                 })

                        );

    //draw the arch and the id of the cluster
            var testoTroncato = convertValue(clusterTree);

            LineRoot(xOldCord, yOldCord, newXCoordinates, newYCoordinates, space2Draw)
          var d=  space2Draw.text(newXCoordinates, newYCoordinates, testoTroncato).attr({ fill: "white" }).mouseover(function (clusterTree) {
               return function () {
                   var tip = $("#tooltip");
                   tip.show();
                   addTip(d.node,tip);
                   $(document).mousemove(function (e) {
                       if (over) {
                           tip.css("left", e.clientX + 20).css("top", e.clientY + 20);
                           tip.text(clusterTree + "");
                       }
                   });
                }
            }(clusterTree));
            st.attr({ fill: "red" });
            if (haFigli === true && isUltimo) {

                newXCoordinates += 300;

            } else {

                newXCoordinates += 112;
            }

            var coordinatesOutput = [newXCoordinates, yOldCord, xOldCord];

      return coordinatesOutput;


}

function addTip(node, tip) {
  
    $(node).mouseenter(function () {
        tip.fadeIn();
        over = true;
    }).mouseleave(function () {
        tip.fadeOut(10);
        over = false;
    });
}

function printUnderTree(clusterTree, xNewCord, yNewCord, xOldCord, yOldCord, space2Draw, haFigli, isUltimo) {
    //Mi sposto a sx dal padre che mi ha chiamato (deve essere uguale tra le due funzioni)
    var newXCoordinates = xNewCord - 80;
    var newYCoordinates = yNewCord + 80;

    space2Draw.circle(newXCoordinates, newYCoordinates, 15).attr({ fill: "white" });;
    LineRoot(xOldCord, yOldCord, newXCoordinates, newYCoordinates, space2Draw);
    space2Draw.text(newXCoordinates, newYCoordinates, "level");


    var xOldCord = newXCoordinates;
    var yOldCord = newYCoordinates;

    for (var i = 0; i < clusterTree.length;i++){
        if (typeof (clusterTree[i]) === "string") {
            if (i === (clusterTree.length-1)) {
                isUltimo = true;
            }
            var coordElement = printElement(clusterTree[i], newXCoordinates, newYCoordinates, xOldCord, yOldCord, space2Draw,  haFigli,isUltimo);
            newXCoordinates = coordElement[0];
            newYCoordinates = coordElement[1];
            xOldCord = coordElement[2];

        } else {
           
            haFigli = true;
            var coord = printUnderTree(clusterTree[i], newXCoordinates, newYCoordinates, xOldCord, yOldCord, space2Draw,  haFigli, isUltimo);
            newXCoordinates = coord;
        }
    
    
    }

    return newXCoordinates+100;


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





function printRoot(space2Draw) {
    //Return the x and y coordinates of the root
    var coordinates = [300, 25];

    var xRadice = 300;
    var yRadice = 25;

    //Print the root
    space2Draw.circle(xRadice, yRadice, 15).attr({ fill: "white" });
    space2Draw.text(xRadice, yRadice, "root");

    return coordinates;


}







//var space2Draw;
//var st;

//var firstX;

//function createTree(cluster_tree, type, description, id, name) {

//    //Nascondo gli input
//    //document.getElementById('inputModelId').value = " ";


//    //Space in which i want to draw 
//    var divResult = document.getElementById('printResult');
//    space2Draw = new Raphael(divResult, 1600, 1000);
//    //Print the root 
//    var coordinatesRoot = printRoot(space2Draw);

//    //coordinates of the circle
//    var xNewCord = coordinatesRoot[0];
//    var yNewCord = coordinatesRoot[1]

//    //coordinates for the arches
//    var xOldCord = coordinatesRoot[0];
//    var yOldCord = coordinatesRoot[1]



//    //Print the description     
//    space2Draw.text(100, 25, "Type: " + type);
//    space2Draw.text(100, 45, "Id: " + id);
//    space2Draw.text(100, 65, "Name: " + name);
//    space2Draw.text(100, 85, "Description: " + description);



//    var ultimoElemento = cluster_tree.length - 1;

//    for (var cont = 0; cont < cluster_tree.length; cont++) {
//        if (typeof (cluster_tree[cont]) === "string") {
//            var coordinates = printElement(cluster_tree[cont], xOldCord, yOldCord, xNewCord, yNewCord, space2Draw, type, description, id, name);
//            xNewCord = coordinates[0];
//            yNewCord = coordinates[2];
//            xOldCord = coordinates[1];
//            yOldCord = coordinates[2];
           
//        } else {
//            if (cont !==0) {
//            xNewCord += 380;
//            } if (cont === ultimoElemento) {
//                xNewCord = xNewCord -20;
//            }
//            var coords = printPartitionedElement(cluster_tree[cont], xOldCord, yOldCord, xNewCord, yNewCord, space2Draw, type, description, id, name);
//            xNewCord = coords;
//        }

       

//    }

//    scroolDiv();

//}



////function that draw an element
//function printElement(valore, xOldCord, yOldCord, xNewCord, yNewCord, space2Draw, type, description, id, name) {
   
//    //Translate the new element
//    var newXCoordinates = xNewCord - 100;
//    var newYCoordinates = yNewCord + 80;

//    var lineatext = convertValue(valore);

//    //st rapresent the set of cirlce
//        st = space2Draw.set();
//        st.push(
//             space2Draw.circle(newXCoordinates, newYCoordinates, 15).click((function (valore) {
//                 return function () {
//                     window.open("index-point.html?id=" + (valore) + "&type=" + type + "&description=" + description + "&name=" + name);
//                 }


//             }(valore))).mouseover(function () {
//                 this.attr({ 'cursor': 'pointer' });
//                 this.attr({ 'opacity': '.50' });
//             }).mouseout(function () {
//                 this.attr({ 'opacity': '1' });
//             })

//                    );

//        //draw the arch and the id of the cluster
//        LineRoot(xOldCord, yOldCord, newXCoordinates, newYCoordinates, space2Draw)
//        space2Draw.text(newXCoordinates, newYCoordinates, lineatext).attr({ fill: "white" });
//        st.attr({ fill: "red" });
    


//    newXCoordinates += 150;

//    //return the x value of the coordinate and the old value of y
//    var coordinates = [newXCoordinates, xOldCord, yOldCord, newYCoordinates];
//    return coordinates;
//}


//var contatoreProfondita;

////recursive function that draw the element
//function printPartitionedElement(valore, xOldCord, yOldCord, xNewCord, yNewCord, space2Draw, type, description, id, name) {
//    var newXCoordinates = xNewCord -100;
//    var newYCoordinates = yNewCord + 80;

//    //Print the white node

//    contatoreProfondita = 1;


//    var levelText = convertValue(valore[0][0], 6 * contatoreProfondita, 3 * contatoreProfondita);
  

//    space2Draw.circle(newXCoordinates, newYCoordinates, 15).attr({ fill: "white" });;
//    LineRoot(xOldCord, yOldCord, newXCoordinates, newYCoordinates, space2Draw);
//    space2Draw.text(newXCoordinates, newYCoordinates, levelText);

//    var xOldCord;
//    var yOldCord;
//    var xCord;
//    var yCord;

//    xOldCord = newXCoordinates;
//    yOldCord = newYCoordinates;
//    xCord = newXCoordinates;
//    yCord = newYCoordinates;

//    var ultimoElemento = valore.length - 1;
    
//    for (var cont = 0; cont < valore.length; cont++) {
//        if (typeof (valore[cont]) === "string") {
//            var coordinatesElement = printElement(valore[cont], xOldCord, yOldCord, xCord, yCord, space2Draw, type, description, id, name);
//            xCord = coordinatesElement[0];
//            yCord = coordinatesElement[2];
//            xOldCord = coordinatesElement[1];
//            yOldCord = coordinatesElement[2];
          

           
//        } else {
           
//            if (cont === ultimoElemento) {
//                xNewCord = xNewCord - 150;
//            }
//            var coord = printPartitionedElement(valore[cont], xOldCord, yOldCord, xCord, yCord, space2Draw, type, description, id, name);
//            xCord = coord;
//            contatoreProfondita++;

//        }

        
//    }


//    return (newXCoordinates + 150);

//}



//function convertValue(value,from,to) {
//    if (typeof(from)==="undefined" && typeof (to)=== "undefined") {
//        var valueLength = value.length;
//        return value.substring(valueLength - 3, valueLength);
//    }
//        else{
        
//        var valueLength = value.length;
//        return value.substring(valueLength - from, valueLength-to);
    
//        }
//}

//function printRoot(space2Draw) {
//    //Return the x and y coordinates of the root
//    var coordinates = [180, 25];

//    var xRadice = 180;
//    var yRadice = 25;

//    //Print the root
//    space2Draw.circle(xRadice, yRadice, 15).attr({ fill: "white" });
//    space2Draw.text(xRadice, yRadice, "root");

//    return coordinates;


//}


