function maintainSelectedTags(action, tag){
    dct = {};
    dct['tag'] = tag;
    dct['action'] = action;
    dct['empty_tag_list'] = 'false';

    $.ajax({
           url: "/search/getGraphData/",
           type: "POST",
           data: dct,
           async: 'false',
           success: function(data) {
               console.log(data);
               createGraph("#graph_div", jQuery.parseJSON(data));
           },
           error:function(data) {
              console.log("Error:"+data.responsetext);
           },
    });
}

function createGraph(element_id, graph_json){
    
    $(element_id).empty();  
    $('#selected_tag_div').empty();

    for(var i=0; i<graph_json['nodes'].length; i++){
        if(graph_json['nodes'][i]['group'] == 1){
            label_str = '<label style="margin-right:10px"><h4><span class="label label-primary">' + graph_json['nodes'][i]['name'] + '</span></h4></label>';
            $('#selected_tag_div').append(label_str);
        }
    }

    var width = 500;
        height = 400;

    var force = d3.layout.force()
        .size([width, height])
        .charge(-900)
        .linkDistance(200)
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
               .attr("class", function(d) {if(d.group==1){return "node fixed";} else {return "node";}})
               .on("dblclick", dblclick)
               .on("click",click)
               .call(drag); 

    node.append("circle")
        .attr("r", 30);
     
    node.append("text")
        .attr("dx", 35)
        .attr("dy", ".35em")
        .text(function(d) { return d.name }); 

    node.classed("fixed", );

    function tick() {
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });
       
        node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; }); 
    }

    function dblclick(d) {
        d3.select(this).classed("fixed", d.fixed = false);
    }

    function click(d){
        if(d.group == 1){
            maintainSelectedTags("remove",d.name);
        }
        else{
            maintainSelectedTags("add",d.name); 
        }
    }

    function dragstart(d) {
        d3.select(this).classed("fixed", d.fixed = true);
    }
}