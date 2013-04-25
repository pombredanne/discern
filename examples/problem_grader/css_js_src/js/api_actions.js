$(function(){
    var tokenValue = $.cookie('problemgradercsrftoken');

    $.ajaxSetup({
        headers: {'X-CSRF-Token': tokenValue}
    });

})

$(function(){
    var model_type = $('#model_name').attr('model');
    var API_BASE = $('#model_name').attr("url");
    if(model_type!=undefined) {
        $.ajax({
            type: "GET",
            url: API_BASE,
            data: { action: "get", model: model_type }
        }).done(function( msg ) {
               console.log(msg)
        });
    }
})