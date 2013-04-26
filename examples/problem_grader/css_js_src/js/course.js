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
    var container_template = $( "#course-list-template" ).html();
    var courses = new Array();
    for (var i = 0; i < data.length; i++) {
        var elem = data[i];
        var mod_course_name = elem.course_name.replace(/ /g, "_");

        var elem_dict = {
            name : elem.course_name,
            href : elem.id + mod_course_name,
            user_count : elem.users.length,
            problem_count: elem.problems.length,
            modified : new Date(Date.parse(elem.modified)),
            created: new Date(Date.parse(elem.created)),
            id : elem.id
        }
        courses.push(_.template(item_template,elem_dict));
    }
    var template_data = {
        courses: courses
    };
    model_data.append(_.template(container_template,template_data))
    add_course_button()
    $('#create-course').click(create_course);
    $('.delete-course').click(delete_course);
    $('.show-problems').click(get_problem);
}

var get_problem = function(target) {
    var target_btn = $(target.target);
    var form = target_btn.parent().parent().parent();
    var inputs = form.find('.accordion-toggle')
    var course_id = inputs.data('elem_id')
    window.location.href = "/grader/problem/?course_id=" + course_id;
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

var get_course_items = function(model_type) {
    var api_base = $('#model_name').attr("url");
    switch(model_type)
    {
        case "course":
            callback = render_course;
            break;
    }
    get_models(api_base, model_type, callback)
}

var delete_course = function(target) {
    var target_btn = $(target.target);
    var data = target_btn.parent();
    var id = data.data('elem_id')
    var api_url = $('#model_name').attr("url") + "/";
    $.ajax({
        type: "POST",
        url: api_url,
        data: { action: "delete", model: 'course', id : id}
    }).done(get_model_type_and_items);
}

var create_course = function(target) {
    var target_btn = $(target.target);
    var form = target_btn.parent().parent().parent();
    var inputs = form.find('input')
    var course_name = inputs.val()
    var api_url = $('#model_name').attr("url") + "/";
    post_data = {
        course_name : course_name
    }
    $.ajax({
        type: "POST",
        url: api_url,
        data: { action: "post", model: 'course', data : JSON.stringify(post_data)}
    }).done(get_model_type_and_items);
}

var get_model_type_and_items = function() {
    var model_type = $('#model_name').attr('model');
    if(model_type!=undefined) {
        get_course_items(model_type)
    }
}

$(function(){
    var tokenValue = $.cookie('problemgradercsrftoken');

    $.ajaxSetup({
        data: {csrfmiddlewaretoken: tokenValue },
        headers: {'X-CSRF-Token': tokenValue}
    });
    get_model_type_and_items()
})