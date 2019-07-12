var svg = d3.select('svg');
svg.attr('width', 500);
data = [10, 15,20];
svg.selectAll('circle')
    .data(data)
    .enter()
    .append('circle')
    .attr('cx', function(){return Math.random() * 360;})
    .attr('cy', 100)
    .attr('fill', 'steelblue')
    .attr('r', function(d){return d;})

var circle = svg.selectAll('circle');
circle.data([20, 50]);
circle.data().exit().remove();
circle.data([20, 50]);

svg.selectAll('path')
    .data()

let rect = svg.selectAll('rect');
rect.enter()
    .append('rect')
    .attr('x', 10)
    .attr('y',100)
    .attr('width', 10)
    .attr('height', 100)
rect.data([10]);
var circle = svg.selectAll("circle")
  .data(data);

circle.exit().remove();

circle.enter().append("circle")
    .attr("r", 2.5)
  .merge(circle)
    .attr("cx", function(d) { return d.x; })
    .attr("cy", function(d) { return d.y; });