let svg = d3.select('svg');
let bar1 = svg.append('rect')
    .attr('x', 100)
    .attr('y', 100)
    .attr('width', 10)
    .attr('fill', 'steelblue')
    .attr('height', 10);

bar1.transition()
    // .ease(d3.easeLinear)
    .duration(1000)
    // .attr('fill', 'red')
    .attr('height', 100)
    .on('end', e =>{
        svg.append('circle')
        .attr('x', 100)
        .attr('y', 100)
        .attr('r', 150);
    })

