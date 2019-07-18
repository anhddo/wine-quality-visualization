let svg = d3.select('svg');
let path = svg.append('path');
let t = d3.transition()
    .duration(1000)
    .ease(d3.easeLinear);

let e = path
    .attr('d', 'M10 10 H 10')
    .attr('stroke-width', 3)
    .attr('stroke', 'blue')
    .attr('fill', 'none');
// .end();
path.transition()
    .duration(1500)
    .ease(d3.easeLinear)
    .attr('d', 'M10 10 H 100')
    .transition()
    .duration(1500)
    .ease(d3.easeLinear)
    .attr('d', 'M10 10 H 100 V 100');
