var pager = {};
list_id = "";

function bindList() {
	var pgItems = pager.pagedItems[pager.currentPage];
	$(list_id).empty();
	for(var i = 0; i < pgItems.length; i++){
	    var option = $('<a class="list-group-item">');
	    for( var key in pgItems[i] ){
		    option.html(pgItems[i][key]);
	      	option.prop('href', "home/utsav/Downloads/admin.py");
	    }
	    $(list_id).append(option);
	}
}

function prevPage(){
    pager.prevPage();
    bindList();
}

function nextPage(){
    pager.nextPage();
    bindList();
}

function pagerInit(p) {
    p.pagedItems = [];
    p.currentPage = 0;
    if (p.itemsPerPage === undefined) {
        p.itemsPerPage = 7;
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

function createFileList(element_id, file_list_json){
	$(element_id).empty();
	list_id = element_id; 
	pager.items = file_list_json;
	pager.itemsPerPage = 5;
	pagerInit(pager);
	bindList();
}