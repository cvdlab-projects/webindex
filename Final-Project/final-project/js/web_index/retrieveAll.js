function allModel() {
    clearDivPreview();
    $(function () {
        $.ajax({ //'http://localhost:28017/ilariomaiolodb/documents/?filter_type=model'
            url:'http://localhost:28017/ilariomaiolodb/documents/?filter_type=model',
            type: 'get',
            dataType: 'jsonp',
            jsonp: 'jsonp', // mongod is expecting the parameter name to be called "jsonp"
            success: function (data) {
                
                //if the document doesn't exist launch an alert
                if (typeof (data) === "undefined") {
                    alert("doesn't exist any model ")
                } else {
                    var length = data["total_rows"]
                    
                    //Retrive clusters_tree 
                    for(var j=0; j<length; j++){
                    var type = data["rows"][j]["type"];
                    var description = data["rows"][j]["description"];
                    var id = data["rows"][j]["id"];
                    var name = data["rows"][j]["name"];
                    
                    createDiv(""+j,type, description, id, name);
                }
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                console.log('error', errorThrown);
            }
        });
    }); 

}

function retriveJsonDocumentById(id) {
    clearDivResult();
    $(function () {
        $.ajax({ // 'http://localhost:28017/ilariomaiolodb/documents/?filter_id=modello'.concat(id)
            url:'http://localhost:28017/ilariomaiolodb/documents/?filter_id=modello'.concat(id),
            type: 'get',
            dataType: 'jsonp',
            jsonp: 'jsonp', // mongod is expecting the parameter name to be called "jsonp"
            success: function (data) {
                
                //if the document doesn't exist launch an alert
                if (typeof (data["rows"][0]) === "undefined") {
                    alert("doesn't exist a model with id : " + id)
                } else {

                    //Retrive clusters_tree 
                    var clustersTree = data["rows"][0]["clusters_tree"];
                    var type = data["rows"][0]["type"];
                    var description = data["rows"][0]["description"];
                    var id = data["rows"][0]["id"];
                    var name = data["rows"][0]["name"];

                    //Print tree
                    createTree(clustersTree, type, description, id, name);
                }
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                console.log('error', errorThrown);
            }
        });
    }); 
}

function over(numberButton){
        var divId =  document.getElementById(""+numberButton);
        divId.style.opacity = ".50";
        divId.style.cursor = "pointer";
        
}

function out(numberButton){
        var divId =  document.getElementById(""+numberButton);
        divId.style.removeProperty("background");
        divId.style.removeProperty("opacity");
               
}



function createDiv(number, type, description, modelloid, name){
    var container = document.getElementById("preview");
    var divId = document.createElement("button");
    divId.setAttribute("id", number);
    divId.setAttribute("width" , "10%");
    divId.setAttribute("height" , "10%");
    divId.setAttribute("float" , "left");
    divId.innerHTML = '<font size='+1+'>description:'+description+'</font>'+
                      '<font size='+1+'>id:'+modelloid+'</font>'+
                      '<font size='+1+'>name:'+name+'</font></br>';
    var id = modelloid.substring(7);
    divId.setAttribute("onclick", "retriveJsonDocumentById("+""+id+")");
    divId.setAttribute("onmouseover","over("+""+number+")");
    divId.setAttribute("onmouseout", "out("+""+number+")")
    container.appendChild(divId);
    
}


function clearDivPreview() {
    var divPreview = document.getElementById('preview');
    divPreview.innerHTML = "";

}