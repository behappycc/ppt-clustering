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
    "台北": 9952.60,
    "嘉義": 4512.66,
    "新竹": 4151.27,
    "基隆": 2809.27,
    "台北": 1932.91,
    "桃園": 1692.09,
    "台中": 1229.62,
    "彰化": 1201.65,
    "高雄": 942.97,
    "台南": 860.02,
    "金門": 847.16,
    "澎湖": 802.83,
    "雲林": 545.57,
    "連江縣": 435.21,
    "新竹": 376.86,
    "苗栗": 311.49,
    "屏東": 305.03,
    "嘉義": 275.18,
    "宜蘭": 213.89,
    "南投": 125.10,
    "花蓮": 71.96,
    "台東": 63.75
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
        //console.log(d.properties.C_Name)
        var data = {
          key1: d.properties.C_Name,
          key2: '2'
        };
        var dataToSend = JSON.stringify(data);
        $.ajax(
          {
              url: '/index',
              type: 'POST',
              data: dataToSend,
              success: function (jsonResponse) {
                var objresponse = JSON.parse(jsonResponse);
                console.log(objresponse['topic']);
                $("#topic").text(objresponse['topic']);
              },
              error: function () {
                $("#topic").text("");
                   }
              });
        });

    }
    d3.select("svg").on("mousemove", function() {
      fisheye.focus(d3.mouse(this));
      update();
    });
    update();
  });
});
