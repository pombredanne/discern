var get_courses = function() {
    $('#problem_nav').empty()
    $('#course_nav').empty()
    var api_base = $('#model_name').attr("url");
    $.ajax({
        type: "GET",
        url: api_base,
        data: { action: "get", model: "course" }
    }).done(render_course_nav);
}

var get_problems = function(course_id) {
    var api_base = $('#model_name').attr("url");
    $.ajax({
        type: "GET",
        url: api_base,
        data: { action: "get", model: "problem" }
    }).done(render_problem_nav_wrapper(course_id));
}

var render_problem_nav_wrapper = function(course_id) {
    var render_problem_nav = function (data) {
        data = $.parseJSON(data);
        problems = new Array();
        for(var z=0; z< data.length ; z++) {
            var problem = data[z]
            for(var i=0;i< problem.courses.length;i++){
                var course_split= problem.courses[i].split("/");
                if(parseInt(course_split[5])==parseInt(course_id)){
                    problems.push(problem);
                }
            }
        }
        var problem_nav_template = $("#problem-nav-template").html()
        var rendered = _.template(problem_nav_template,{problems : problems, course_id : course_id})
        var problem_nav = $("#problem_nav")
        problem_nav.empty()
        problem_nav.html(rendered)
    };
    return render_problem_nav
}

var render_course_nav = function(data) {
    var add_template = $( "#course-nav-template" ).html();
    var course_nav = $('#course_nav')
    data = $.parseJSON(data);
    console.log(data)
    course_nav.html(_.template(add_template,{courses : data}))
    $('.course-select').click(get_problem_nav);
}

var get_problem_nav = function(data) {
    var target = $(data.target).parent();
    var course_id = parseInt(target.data('course_id'))
    get_problems(course_id)
}

$(function(){
    var tokenValue = $.cookie('problemgradercsrftoken');

    $.ajaxSetup({
        data: {csrfmiddlewaretoken: tokenValue },
        headers: {'X-CSRF-Token': tokenValue}
    });
    get_courses()
})