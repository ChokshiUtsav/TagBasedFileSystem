function approve_order(order_id){
	
	$.get('/restaurant/approve_order/?order_id=' + order_id, function(data){

	});
	alert("Order Approved!!")
	location.reload();
}
function decline_order(order_id){

	$.get('/restaurant/decline_order/?order_id=' + order_id, function(data){
		
	});
	alert("Order Declined!!")
	location.reload();  
}

function deliver_order(order_id){
	// alert("in function")
	alert(order_id)
	$.get('/restaurant/deliver_the_order/?order_id=' + order_id, function(data){		
	});
	alert("Order Delivered!!")
	location.reload();  
}
function assign_delivery_boy(order_id){
	// alert("gdj;")
	// delivery_boy_id=1
	var delivery_boy_id = $('[name="available_delivery_boys"]').attr('value');
	alert(delivery_boy_id)
	// alert(delivery_boy_id)
	$.get('/restaurant/assign_delivery_boy/?order_id=' + order_id +'&delivery_boy_id=' + delivery_boy_id, function(data){
		
	});
	// alert("Order Declined!!")
	location.reload();  
}
