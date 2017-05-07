var pager = {};
list_id = "";

function fileNameShortner(file_name){
    var chunks = file_name.toString().split("/");    
    len = chunks.length - 1;       //File Path starts with / so we get an empty element as first element
    var short_file_name = "";
    var upper_limit =  3;

    for(var i=1; i<upper_limit; i++){
        short_file_name += "/";
        short_file_name += chunks[i];
    }

    if(len > 4){
        short_file_name += "/...";
    }

    var lower_limit = len - 1;

    if(len == 3){
        lower_limit = len;
    }
    else if(chunks.length == 2){
        lower_limit = len + 1;
    }

    for(var i=lower_limit; i<=len; i++){
        short_file_name += "/";
        short_file_name += chunks[i];
    }

    return short_file_name;
}

function createHTMLForHome(file_name){
    var html_str = "";
    html_str += '<label style="margin-top:10px" data-toggle="tooltip" data-placement="bottom" title="';
    html_str +=  file_name + '">' + fileNameShortner(file_name) + "</label>";
    html_str += '<button class="btn btn-primary btn-sm" data-toggle="tooltip" data-placement="bottom" title="Manually Assign" type="button" id="manual_assign" style="float:right;margin-left:10px;margin-top:10px"';
    html_str += ' name="' + file_name + '">'; 
    html_str += '<span class="glyphicon glyphicon glyphicon-cog" aria-hidden="true"></span>';
    html_str += '</button>';
    html_str += '<button class="btn btn-primary btn-sm" data-toggle="tooltip" data-placement="bottom" title="Auto Assign" type="button" id="auto_assign" style="float:right;margin-left:10px;margin-top:10px"';
    html_str += ' name="' + file_name + '">';
    html_str += '<span class="glyphicon glyphicon glyphicon-plane" aria-hidden="true"></span>';
    html_str += '</button>';
    html_str += '</li>';
    return html_str;
}

function createHTMLForSearch(file_name){
    var html_str = "";
    html_str += '<label style="margin-top:10px" data-toggle="tooltip" data-placement="bottom" title="';
    html_str +=  file_name + '">' + fileNameShortner(file_name) + "</label>";
    html_str += '</li>';
    return html_str;
}

function bindList(parent_page) {
	var pgItems = pager.pagedItems[pager.currentPage];
	$(list_id).empty();

    for(var i = 0; i < pgItems.length; i++){
        var option = $('<li class="list-group-item" style="overflow:hidden;">');
        for(var key in pgItems[i] ){
            if(parent_page == "home"){
                option.html(createHTMLForHome(pgItems[i][key]));
            }
            else if(parent_page == "search"){
                option.html(createHTMLForSearch(pgItems[i][key]));  
            }
        }
        $(list_id).append(option);
    }
}

function prevPage(parent_page){
    pager.prevPage();
    bindList(parent_page);
}

function nextPage(parent_page){
    pager.nextPage();
    bindList(parent_page);
}

function pagerInit(p) {
    p.pagedItems = [];
    p.currentPage = 0;
    if (p.itemsPerPage === undefined) {
        p.itemsPerPage = 5;
    }
    
    p.prevPage = function(){
		if (p.currentPage > 0){
        	p.currentPage--;
        }
    };
    
    p.nextPage = function(){
        if (p.currentPage < p.pagedItems.length - 1) {
    	    p.currentPage++;
        }
    };
    
    init = function(){
        for (var i = 0; i < p.items.length; i++){
          	if (i % p.itemsPerPage === 0) {
            	p.pagedItems[Math.floor(i / p.itemsPerPage)] = [p.items[i]];
          	}
          	else {
            	p.pagedItems[Math.floor(i / p.itemsPerPage)].push(p.items[i]);
          	}
        }
    };
    
    init();
}

function createFileList(element_id,file_list_json,parent_page){
	$(element_id).empty();
	list_id = element_id; 
	pager.items = file_list_json;
	pager.itemsPerPage = 5;
	pagerInit(pager);
	bindList(parent_page);
}