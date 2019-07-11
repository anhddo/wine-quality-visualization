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
circle.exit().remove();

svg.selectAll('path')
    .data()