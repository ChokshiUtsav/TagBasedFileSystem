$(document).ready(function() {
    $("div.bhoechie-tab-menu>div.list-group>a").click(function(e) {
        e.preventDefault();
        $(this).siblings('a.active').removeClass("active");
        $(this).addClass("active");
        var index = $(this).index();
        $("div.bhoechie-tab>div.bhoechie-tab-content").removeClass("active");
        $("div.bhoechie-tab>div.bhoechie-tab-content").eq(index).addClass("active");
    });
});

function payNow() {
    var checkBox = document.getElementsByName("radio");

    console.log(checkBox);
     if(checkBox == null || checkBox == undefined){
        $('.pop-outer').fadeIn('slow');
        return;
    }
    window.location.href = '/order/pay';
}

function closemsg(){
    $('.pop-outer').fadeOut('slow');
}