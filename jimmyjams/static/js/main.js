// Get playlist info
var retrieveData = function(e){
    $.ajax({
        url: "/playlist_info",
        type: "GET",
        data: {},
        success: function(d) {
            d = JSON.parse(d);
            songs = d["songs"];
            updateData(songs);
        }
    })
};

// display playlist info
var updateData = function(songs){
    clear();
    var div = document.getElementById("songs");
    var element = document.createElement("h3");
    var text = "";
    
    for (i = 0; i < songs.length; i++) { 
        element = document.createElement("h3");
        element.setAttribute("style", "text-align: left;");
        text = document.createTextNode(songs[i][0] + " by " + songs[i][1] + " added by " + songs[i][2]);
        element.appendChild(text);
        div.appendChild(element);
    }  
    
};

var clear = function(){
    var div = document.getElementById("songs");
    while (div.firstChild) {
        div.removeChild(div.firstChild);
    }
};

retrieveData();
setInterval(retrieveData, 3000);