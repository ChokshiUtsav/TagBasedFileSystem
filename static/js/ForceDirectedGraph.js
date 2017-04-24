function createGraph(element_id, graph_json){
    
    $(element_id).empty();  

    var width = 500;
        height = 400;

    var force = d3.layout.force()
        .size([width, height])
        .charge(-400)
        .linkDistance(150)
        .on("tick", tick);

    var drag = force.drag()
        .on("dragstart", dragstart);

    var svg = d3.select(element_id).append("svg")
        .attr("width", width)
        .attr("height", height);

    var link = svg.selectAll(".link"),
        node = svg.selectAll(".node");

    var graph = graph_json;    
   
    force.nodes(graph.nodes)
         .links(graph.links)
         .start();

    link = link.data(graph.links)
               .enter().append("line")
               .attr("class", "link");

    node = node.data(graph.nodes)
               .enter().append("g")
               .attr("class", "node")
               .on("dblclick", dblclick)
               .call(drag); 

    node.append("circle")
        .attr("r", 30);
     
    node.append("text")
        .attr("dx", 35)
        .attr("dy", ".35em")
        .text(function(d) { return d.name });    

    function tick() {
      link.attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });
     
      node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; }); 
      //node.attr("cx", function(d) { return d.x; })
      //    .attr("cy", function(d) { return d.y; });
    }

    function dblclick(d) {
      d3.select(this).classed("fixed", d.fixed = false);
    }

    function dragstart(d) {
      d3.select(this).classed("fixed", d.fixed = true);
    }
}