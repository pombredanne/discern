
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
    data = $.parseJSON(data);
    var item_template = $( "#course-item-template" ).html();
    console.log(item_template)
    var container_template = $( "#course-list-template" ).html();
    var courses = new Array();
    for (var i = 0; i < data.length; i++) {
        var elem = data[i];
        var elem_dict = {
            name : elem.course_name,
            href : elem.id + elem.course_name
        }
        courses.push(_.template(item_template,elem_dict));
    }
    var template_data = {
        courses: courses
    };
    model_data.append(_.template(container_template,template_data))
    add_course_button()
}

var add_course_button = function() {
    var model_add = $("#model_add")
    model_add.empty()
    var add_template = $( "#course-add-template" ).html();
    var add_dict = {
        name : "Add a course",
        href: "course-add"
    }
    model_add.html(_.template(add_template,add_dict))
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