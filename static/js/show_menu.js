// Handle all menu page functionalities

displayCart();

function increment(item_id){
    var num = parseInt($('#' + item_id).text());
    $('#' + item_id).text(num+1);
}

function decrement(item_id){
    var num = parseInt($('#' + item_id).text());
    if(num>1)
        $('#' + item_id).text(num-1);
}


// Add item to cart
function addToCart(item_id, item_name, price){
    var num = parseInt($('#' + item_id).text());
    if(localStorage.getItem('cart')==null)
        var temp = [];
    else
        var temp = JSON.parse(localStorage.getItem('cart'));
    var flag = 0;
    var arrayLength = temp.length;
    if(arrayLength){
        for(var i=0; i<arrayLength; i++){
            if(temp[i]['id'] == item_id){
                temp[i]['quantity']+=num;
                flag = 1;
            }
        }
    }
    if(!flag){
        var item_dict = {'id':item_id, 'item_name':item_name, 'quantity':num, 'price':price};
        temp.push(item_dict);
    }
    console.log(temp);
    localStorage.setItem('cart', JSON.stringify(temp));
    printCart();
}
function printCart() {
    var cartContainer = document.getElementById('cart');
    var cardTheme = "<div class='card'><div class='card-block'><h4 class='card-title'>My Cart</h4>";
    var str = "<p class='card-text'>";
    var cartData = JSON.parse(localStorage.getItem('cart'));
    if(cartData) {
        for (var ii = 0; ii < cartData.length; ii++) {
            str += cartData[ii].item_name + ":" + cartData[ii].quantity + "<br>"
        }
    } else {
        str += "<span style='background-color: transparent'><img style='opacity: 0.3;' src='https://www.shareicon.net/data/128x128/2016/07/15/796506_delivery_512x512.png'></span><br><span class='no-items-text'>Add Some Food into Your Cart</span>"
    }
    str += "</p></div></div>";
    cartContainer.innerHTML = str;
}
function checkout(){
    //if(request.user.is_authenticated()){
    //    var data = {'cart': localStorage.getItem('cart'), 'restaurant_id': localStorage.getItem('restaurant_id')};
    //    $.post('/order/createOrder',data,function(response){
    //        console.log(response);
    //    });
    //}
    //else{
    if(localStorage.getItem('cart')==null || localStorage.getItem('cart')== undefined){
        //$('#exampleModal3').modal('show');
        $('.pop-outer').fadeIn('slow');
        return;
    }
       window.location.href = '/order/review';
    //}
}

function displayCart(){
    if(localStorage.getItem('restaurant_id')==null)
        localStorage.setItem('restaurant_id', getQueryStringValue("restaurant_id"));
    else if(localStorage.getItem('restaurant_id')==getQueryStringValue("restaurant_id"))
        if(localStorage.getItem('cart'))
            document.getElementById("cart").innerHTML = localStorage.getItem('cart');
    else{
        localStorage.setItem('restaurant_id', getQueryStringValue("restaurant_id"));
        if(localStorage.getItem('cart'))
            localStorage.removeItem('cart');
    }
}

function getQueryStringValue (key) {  
  return decodeURIComponent(window.location.search.replace(new RegExp("^(?:.*[&\\?]" + encodeURIComponent(key).replace(/[\.\+\*]/g, "\\$&") + "(?:\\=([^&]*))?)?.*$", "i"), "$1"));  
}
function clearcart() {
    if(localStorage.getItem('cart')!=null){
        localStorage.removeItem('cart');
    }
    printCart();
}
function closemsg(){
    $('.pop-outer').fadeOut('slow');
}