$(function(){
    var tokenValue = $.cookie('problemgradercsrftoken');

    $.ajaxSetup({
        headers: {'X-CSRF-Token': tokenValue}
    });

})

var get_models = function(api_url, model_type, callback) {
    $.ajax({
        type: "GET",
        url: api_url,
        data: { action: "get", model: model_type }
    }).done(callback);
 }

var render_course = function(data) {
    var model_data = $("#model_container");
    model_data.empty();
    data = $.parseJSON(data)
    var template = _.template(
        $( "#course-item-template" ).html()
    );
    for (var i = 0; i < data.length; i++) {
        var elem = data[i];
        console.log(elem);
        model_data.append(elem.course_name);
    }
    add_course_button()
}

var add_course_button = function() {
    var model_add = $("#model_add")
    model_add.empty()
    model_add.html('<button class="btn btn-primary" id="course_add">Add new course</button>')
}

$(function(){
    var model_type = $('#model_name').attr('model');
    var API_BASE = $('#model_name').attr("url");
    var callback = function (msg) {
        console.log(msg);

    }
    if(model_type!=undefined) {
        get_models(API_BASE, model_type, render_course)
    }
})