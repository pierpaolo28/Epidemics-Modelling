document.addEventListener('DOMContentLoaded', function(e) {

  let svg = d3.select('#vis').append("svg")
    .attr("width", "80%")
    .attr("height", "80%")
    .attr("viewBox", "0 0 500 500");

  let img = svg.append("svg:image")
    .attr("xlink:href", "./first.PNG")
    .attr("width", "80%")
    .attr("height", "80%")

  function draw1(svg) {
    d3.select("#vis").selectAll("svg").remove();

    let svg2 = d3.select('#vis').append("svg")
      .attr("width", "80%")
      .attr("height", "80%")
      .attr("viewBox", "0 0 500 500");

    let img2 = svg2.append("svg:image")
      .attr("xlink:href", "./first.PNG")
      .attr("width", "80%")
      .attr("height", "80%")

    return svg2
  }

  function draw2(svg) {

    d3.select("#vis").selectAll("svg").remove();

    let svg2 = d3.select('#vis').append("svg")
      .attr("width", "80%")
      .attr("height", "80%")
      .attr("viewBox", "0 0 500 500");

    let img2 = svg2.append("svg:image")
      .attr("xlink:href", "./two.PNG")
      .attr("width", "80%")
      .attr("height", "80%")

    return svg2
  }

  function draw3(svg) {

    d3.select("#vis").selectAll("svg").remove();

    let svg2 = d3.select('#vis').append("svg")
      .attr("width", "80%")
      .attr("height", "80%")
      .attr("viewBox", "0 0 500 500");

    let img2 = svg2.append("svg:image")
      .attr("xlink:href", "./abflow.PNG")
      .attr("width", "80%")
      .attr("height", "80%")

    return svg2
  }

  function draw4(svg) {

    d3.select("#vis").selectAll("svg").remove();

    let svg2 = d3.select('#vis').append("svg")
      .attr("width", "80%")
      .attr("height", "80%")
      .attr("viewBox", "0 0 500 500");

    let img2 = svg2.append("svg:image")
      .attr("xlink:href", "./abtest.PNG")
      .attr("width", "80%")
      .attr("height", "80%")

    return svg2
  }

  function draw5(svg) {

    d3.select("#vis").selectAll("svg").remove();

    let svg2 = d3.select('#vis').append("svg")
      .attr("width", "80%")
      .attr("height", "80%")
      .attr("viewBox", "0 0 500 500");

    let img2 = svg2.append("svg:image")
      .attr("xlink:href", "./abtest2.PNG")
      .attr("width", "80%")
      .attr("height", "80%")

    return svg2
  }

  function draw6(svg) {

    d3.select("#vis").selectAll("svg").remove();

    let svg2 = d3.select('#vis').append("svg")
      .attr("width", "80%")
      .attr("height", "80%")
      .attr("viewBox", "0 0 500 500");

    let img2 = svg2.append("svg:image")
      .attr("xlink:href", "./WBS.PNG")
      .attr("width", "80%")
      .attr("height", "80%")

    return svg2
  }


  //Array of all the graph functions
  //Will be called from the scroller functionality

  let activationFunctions = [
    draw1,
    draw2,
    draw3,
    draw4,
    draw5,
    draw6
  ]

  //All the scrolling function
  //Will draw a new graph based on the index provided by the scroll

  let scroll = scroller()
    .container(d3.select('#graphic'))
  scroll()

  let lastIndex, activeIndex = 0

  scroll.on('active', function(index) {
    d3.selectAll('.step')
      .transition().duration(500)
      .style('opacity', function(d, i) {
        return i === index ? 1 : 0.1;
      });

    activeIndex = index
    let sign = (activeIndex - lastIndex) < 0 ? -1 : 1;
    let scrolledSections = d3.range(lastIndex + sign, activeIndex + sign, sign);
    scrolledSections.forEach(i => {
      svg = activationFunctions[i](svg);
    })
    lastIndex = activeIndex;

  })

  scroll.on('progress', function(index, progress) {
    if (index == 2 & progress > 0.7) {

    }
  })

});