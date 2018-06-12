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
    var element = document.createElement("div");
    var inner = "";
    var text = "";
    
    for (i = 0; i < songs.length; i++) { 
        element = document.createElement("div");
        element.className = "card card-stack";
        inner = document.createElement("h3");
        inner.setAttribute("style", "text-align: left;");
        text = document.createTextNode(songs[i][0].bold() + " by " + songs[i][1]);
        spa = document.createElement("span");
        spa.setAttribute("style","float: right;");
        spa = document.createTextNode(songs[i][2]);
        inner.appendChild(text);
        inner.appendChild(spa);
        element.appendChild(inner);
        div.appendChild(element);
    }  
    
    if (songs.length < 1){
        element = document.createElement("h3");
        element.setAttribute("style", "text-align: center;");
        text = document.createTextNode("No songs have been added.")
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
