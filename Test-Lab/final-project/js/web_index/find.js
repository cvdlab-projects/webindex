function retriveJsonDocument() {
    clearDivResult();
  
	 $(function () {
         var value = document.getElementById('inputModelId').value;
         $.ajax({ 
             url: 'http://localhost:28017/ilariomaiolodb/documents/?filter_id=' + value,
             type: 'get',
             dataType: 'jsonp',
             jsonp: 'jsonp', // mongod is expecting the parameter name to be called "jsonp"
             success: function (data) {
                
                 //if the document doesn't exist launch an alert
                 if (typeof (data["rows"][0]) === "undefined") {
                     alert("doesn't exist a model with id : " + value);
                 } else {

                    //Retrive clusters_tree 
                     var clustersTree = data["rows"][0]["clusters_tree"];
                     console.log(clustersTree);
                     //Scrivo sulla pagina html tutti gli id dei cluster

                     var name = data["rows"][0]["name"];
                     var dimension = data["rows"][0]["dimension"];
                     var id = data["rows"][0]["id"];
                     var description = data["rows"][0]["description"];

                    //Print tree
                     createTree(clustersTree, dimension, description, id, name);
                 }
             },
             error: function (XMLHttpRequest, textStatus, errorThrown) {
                 console.log('error', errorThrown);
             }
         });
     }); 
}


























function clearDivResult() {
    var divResult = document.getElementById("printResult");
    var svg = document.getElementsByTagName("svg")[0];
    if(svg==null)
        return false;
    else{
    divResult.removeChild(svg);
    }
}




    //function retriveIdTooltip(cluster){
    //    var div = document.getElementById("tooltip");
      
    //    for (var i = 0 ; i < cluster.length ; i++) {
    //        var newParagraph = document.createElement("p");
    //        var textParagraph = document.createTextNode(cluster[i]);
    //        newParagraph.appendChild(textParagraph);
    //        div.appendChild(newParagraph);
           
    //        document.body.appendChild(newParagraph);
    //    }
        
    //}

