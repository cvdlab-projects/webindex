function retriveIdCluster() {

    var queryString = location.search;
    var id;
    if (queryString) {
        id = queryString.split("?");
        id = id[1].split("=");
        id = id[1].split("&");
        return id[0];


    } else {

        alert("Id del Cluster non trovato nel query string");

    }


}



function retrieveCluster() {


    var idCluster = retriveIdCluster();

     $(function () {
        $.ajax({ 
            url: 'http://localhost:28017/ilariomaiolodb/documents/?filter_id=0',
            type: 'get',
            dataType: 'jsonp',
            jsonp: 'jsonp', // mongod is expecting the parameter name to be called "jsonp"
            success: function (data) {

                var result = data["rows"][0];
                var vertices = result["points"];
                var vertices_transformation = result["location"];

                console.log(result);
                console.log(vertices);
                console.log(vertices_transformation);

                if (typeof (vertices) === "undefined" || typeof (vertices_transformation) === "undefined") {
                    alert("SI E' VERIFICATO UN ERRORE!");

                } else {
                    

                    var point = coordsTransformation(vertices, vertices_transformation);
                
                    Draw(point);

                    }
 
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                //console.log('error', errorThrown);
				alert("SI E' VERIFICATO UN ERRORE DI RETE")
            }
        });
  
    });

}


function Draw(vertici) {
    for (var i = 0; i < vertici.length ; i++) {
        var ar = [];
        ar.push(vertici[i])
        var point = POLYPOINT(ar);
        DRAW(point);
        console.log("draw")
    }
}




function coordsTransformation(retrivedPoints,retrivedLocation) {
 
        var points = retrivedPoints;
        var location = retrivedLocation;

        var xLoc = location[0];
        var yLoc = location[1];
        var zLoc = location[2];
        var transPoints = [];
  
        for(var i = 0; i < points.length; i++){
            for(var j = 0; j < points[i].length; j++){
                var point = [ points[i][j][0] + xLoc, points[i][j][1] + yLoc, zLoc + i ];
                transPoints.push(point);
            }

        }

        
        return transPoints;

    
}



