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
        text = document.createTextNode(songs[i][0] + " by " + songs[i][1] + " added by " + songs[i][2]);
        inner.appendChild(text);
        remove = document.createElement("form");
        remove.setAttribute("action", "/remove_track");
        remove.setAttribute("method", "POST");
        song = document.createElement("input");
        song.setAttribute("type", "hidden");
        song.setAttribute("name", "song");
        song.setAttribute("value", songs[i][0]);
        artist = document.createElement("input");
        artist.setAttribute("type", "hidden");
        artist.setAttribute("name", "artist");
        artist.setAttribute("value", songs[i][1]);
        button = document.createElement("button");
        button.setAttribute("type", "submit");
        button.innerHTML = "Remove";
        button.className = "btn";
        remove.appendChild(song);
        remove.appendChild(artist);
        remove.appendChild(button);
        element.appendChild(inner);
        element.appendChild(remove);
        div.appendChild(element);
    }

    if (songs.length < 1){
        element = document.createElement("h3");
        element.setAttribute("style", "text-align: center;");
        text = document.createTextNode("No songs have been added.");
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
