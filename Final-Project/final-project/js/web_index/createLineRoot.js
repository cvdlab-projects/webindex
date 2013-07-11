//Creo una funzione che genera gli archi per la root)
function LineRoot(startX, startY, endX, endY, raphael) {
    var start = {
        x: startX,
        y: startY+15 
    };
    var end = {
        x: endX,
        y: endY-15
    };
    var getPath = function () {
        return "M" + start.x + " " + start.y + " L" + end.x + " " + end.y;
    };
    var redraw = function () {
        node.attr("path", getPath());
    }

    var node = raphael.path(getPath());
    node.id = "id";
    
    return {
        updateStart: function (x, y) {
            start.x = x;
            start.y = y;
            redraw();
            return this;
        },
        updateEnd: function (x, y) {
            end.x = x;
            end.y = y;
            redraw();
            return this;
        }
       
    };

   

};