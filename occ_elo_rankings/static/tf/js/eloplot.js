var dataset = [ 5, 10, 15, 20, 25, 12, 12 ,42, 12, 13 ];
var barPadding = 2;

//Width and height
var w = 500;
var h = 50;

var svg = d3.select("#eloplot")
            .append("svg")
            .attr("width", w)
            .attr("height", h);

svg.selectAll("rect")
    .data(dataset)
    .enter()
    .append("rect")
    .attr("x", 0)
    .attr("y", function(d) {
        return h - d;  //Height minus data value
    })
    .attr("width", w / dataset.length - barPadding)
    .attr("height", function(d) {
        return d;  //Just the data value
    })
    .attr("x", function(d, i) {
      return i * (w / dataset.length);
      })
    .attr("height", function(d) {
      return d;
      })
    .attr("fill", "teal");
