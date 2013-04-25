API_BASE = "http://127.0.0.1/"
API_PATH = API_BASE + "essay_site/api/v1/"

$(function(){
    var tokenValue = $.cookie('csrftoken');

    $.ajaxSetup({
        headers: {'X-CSRF-Token': tokenValue}
    });

})

$(function(){
    model_type = $('#model_name').attr('model');
    if(model_type!=undefined) {
        $.ajax({
            type: "GET",
            url: API_PATH + model_type + "/?format=json"
        }).done(function( msg ) {
                
        });
    }
})