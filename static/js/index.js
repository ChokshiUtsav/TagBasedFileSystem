// Handle all index page functionalities

$(document).ready(function(){
    loadAreas();
    $('[name="city"]').change(loadAreas);
    
    // Load selected city's areas
    function loadAreas(){
        var city = $('[name="city"]').attr('value');
        $.get('/restaurant/get_areas/?city=' + city, function(data){
            $('[name="area"]').empty();
            $.each(JSON.parse(data), function(val, text){
                $('[name="area"]').append( $('<option></option>').val(text['fields']['area']).html(text['fields']['area']));
            });
        });
    }
});