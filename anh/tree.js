function duplicate_text(selector, n = 10) {
    let lorem_html = $(selector).html();
    let text = '';
    console.log(lorem_html);
    for (let i = 0; i < n; i++) {
        text += lorem_html;
    }
    $(selector).html(text);
}

function anim(selector){

    data = [[10, 10], [100, 10], [100, 200]]
    let p = d3.line()(data)
    let svg = d3.select('svg');
    let path = svg.append('path')
        .attr('d', p)
        .attr('stroke-width', 3)
        .attr('stroke', 'red')
        .attr('fill', 'none');
    let path_length = path.node().getTotalLength();
    path.attr('stroke-dasharray', path_length)
    let container = $('.container');
    let container_height = container.outerHeight();
    path.attr('stroke-dashoffset', path_length);
    let scrollable_value = container_height - window.innerHeight;
    scrollable_value = ($('#tree').height() - window.innerHeight) * 3 / 4;
    window.addEventListener('scroll', function () {
        let scroll_value = document.getElementsByTagName('body')[0].scrollTop;
        let i = path_length * (scrollable_value - scroll_value) / scrollable_value;
        // this.console.log(i, scroll_value, container_height);˝
        if (i < 0) {
            i = 0;
        }
        path.attr('stroke-dashoffset', i);
    });
}

$(function () {
    duplicate_text('#tree');
    duplicate_text('#about', 20)
    // anim('svg-1');
    // anim('svg-2');
    
});