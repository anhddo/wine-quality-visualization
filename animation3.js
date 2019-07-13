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
let container_height = document.getElementById('container').offsetHeight;
path.attr('stroke-dashoffset', 300);
window.addEventListener('scroll', function () {
    let scroll_value = document.getElementsByTagName('body')[0].scrollTop;
    let i = 300 * (container_height - scroll_value) / container_height;
    path.attr('stroke-dashoffset', i);
});