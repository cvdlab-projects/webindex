//Creo una funzione che genera gli archi del mio albero (esclusa la root)
function LineChildren(startX, startY, endX, endY, raphael) {
    var start = {

        //-20 altrimenti le linee sarebbero centrate nel cerchio
        x: startX,
        y: startY-20
    };
    var end = {
        //+20 altrimenti le linee sarebbero centrate nel cerchio
        x: endX,
        y: endY+20
    };
    var getPath = function () {
        return "M" + start.x + " " + start.y  + " L" + end.x + " " + end.y;
    };
    var redraw = function () {
        node.attr("path", getPath());
    }

    var node = raphael.path(getPath());
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