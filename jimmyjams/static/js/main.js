// Get playlist info
var retrieveData = function(e){
  $.ajax({
    url: "/playlist_info",
    type: "GET",
    data: {},
    success: function(d) {
      d = JSON.parse(d);
      key = d["word"];
      bankSize = d["bank_length"];
      setUp();
    }
  })
};