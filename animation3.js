data = [[10, 10], [100, 10], [100, 200]]
let p = d3.line()(data)
let svg = d3.select('svg');
let path = svg.append('path')
    .attr('d', p)
    .attr('stroke-dasharray', '300 300')
    .attr('stroke-width', 3)
    .attr('stroke', 'red')
    .attr('fill', 'none');
let i = 300;
d3.select('body')
    .on('keydown', () => {
        console.log('down');
        i--
        path
            .attr('stroke-dashoffset', i);
    })