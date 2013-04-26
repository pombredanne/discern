var get_courses = function() {
    var api_base = $('#model_name').attr("url");
    $.ajax({
        type: "GET",
        url: api_base,
        data: { action: "get", model: "course" }
    }).done(render_course_nav);
}

var render_course_nav = function(data) {
    var add_template = $( "#course-nav-template" ).html();
    var course_nav = $('#course_nav')
    data = $.parseJSON(data);
    console.log(data)
    course_nav.html(_.template(add_template,{courses : data}))
}

$(function(){
    var tokenValue = $.cookie('problemgradercsrftoken');

    $.ajaxSetup({
        data: {csrfmiddlewaretoken: tokenValue },
        headers: {'X-CSRF-Token': tokenValue}
    });
    get_courses()
})