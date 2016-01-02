$(document).ready(function() {
      $('.parallax').parallax();

      $("#btn_Run").click(function(){
        alert("hello fatty");
      });

      /*
      $('#runajax').click(function (event) {

                var valueForInput1 = $("#input1").val();
                var valueForInput2 = $("#input2").val();

                var data =
                {
                    key1: valueForInput1,
                    key2: valueForInput2
                };

                var dataToSend = JSON.stringify(data);

                $.ajax(
                        {
                            url: '/testajax',
                            type: 'POST',
                            data: dataToSend,

                            success: function (jsonResponse) {
                                var objresponse = JSON.parse(jsonResponse);
                                console.log(objresponse['newkey']);

                                $("#responsefield").text(objresponse['newkey']);

                            },
                            error: function () {
                                $("#responsefield").text("Error to load api");

                            }
                        });

                event.preventDefault();
            });
*/

  var density = {
    "臺北市": 9952.60,
    "嘉義市": 4512.66,
    "新竹市": 4151.27,
    "基隆市": 2809.27,
    "新北市": 1932.91,
    "桃園市": 1692.09,
    "臺中市": 1229.62,
    "彰化縣": 1201.65,
    "高雄市": 942.97,
    "臺南市": 860.02,
    "金門縣": 847.16,
    "澎湖縣": 802.83,
    "雲林縣": 545.57,
    "連江縣": 435.21,
    "新竹縣": 376.86,
    "苗栗縣": 311.49,
    "屏東縣": 305.03,
    "嘉義縣": 275.18,
    "宜蘭縣": 213.89,
    "南投縣": 125.10,
    "花蓮縣": 71.96,
    "臺東縣": 63.75
  };
  d3.json("static/json/county.json", function(topodata) {
    var features = topojson.feature(topodata, topodata.objects.county).features;
    var color = d3.scale.linear().domain([0,10000]).range(["#090","#f00"]);
    var fisheye = d3.fisheye.circular().radius(100).distortion(2);
    var prj = function(v) {
      var ret = d3.geo.mercator().center([122,23.25]).scale(6000)(v);
      var ret = fisheye({x:ret[0],y:ret[1]});
      return [ret.x, ret.y];
    };
    var path = d3.geo.path().projection(prj);
    for(idx=features.length - 1;idx>=0;idx--) features[idx].density = density[features[idx].properties.C_Name];
    d3.select("svg").selectAll("path").data(features).enter().append("path");
    function update() {
      d3.select("svg").selectAll("path").attr({
        "d": path,
        "fill": function (d) { return color(d.density); }
      }).on("mouseover", function(d) {
        $("#name").text(d.properties.C_Name);
        $("#density").text(d.density);

      });
    }
    d3.select("svg").on("mousemove", function() {
      fisheye.focus(d3.mouse(this));
      update();
    });
    update();
  });
});
