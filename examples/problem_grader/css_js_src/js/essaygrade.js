var get_courses = function() {
    $('#problem_nav').empty()
    $('#course_nav').empty()
    $('#essay-container').empty()
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
        $('.problem-select').click(get_essay_list);
    };
    return render_problem_nav
}

var render_course_nav = function(data) {
    var add_template = $( "#course-nav-template" ).html();
    var course_nav = $('#course_nav')
    data = $.parseJSON(data);
    course_nav.html(_.template(add_template,{courses : data}))
    $('.course-select').click(get_problem_nav);
}

var get_problem_nav = function(data) {
    var target = $(data.target).parent();
    var course_id = parseInt(target.data('course_id'))
    get_problems(course_id)
}

var render_essay_wrapper = function(prompt, problem_id) {
    var render_essay = function(data) {
        var model_data = $("#essay-container");
        model_data.empty();
        data = $.parseJSON(data);
        var item_template = $( "#essay-item-template" ).html();
        var container_template = $( "#essay-list-template" ).html();
        var essays = new Array();
        for (var i = 0; i < data.length; i++) {
            var elem = data[i];
            console.log(elem)
            var essay_name = "Essay with id " + elem.id.toString();
            var mod_essay_name = essay_name.replace(/ /g, "_");

            var elem_dict = {
                name : essay_name,
                prompt : prompt,
                href : mod_essay_name,
                modified : new Date(Date.parse(elem.modified)),
                created: new Date(Date.parse(elem.created)),
                id : elem.id,
                essay_text : elem.essay_text
            }
            var problem = elem.problem
            var problem_split=problem.split("/");
            if(parseInt(problem_split[5])==problem_id){
                essays.push(_.template(item_template,elem_dict));
            }
        }
        var template_data = {
            essays: essays
        };
        model_data.append(_.template(container_template,template_data))
    }
    return render_essay
}

var get_essay_list = function(data) {
    var target = $(data.target).parent();
    var problem_id = parseInt(target.data('problem_id'));
    var prompt = target.data('prompt');

    var api_base = $('#model_name').attr("url");
    $.ajax({
        type: "GET",
        url: api_base,
        data: { action: "get", model: "essay" }
    }).done(render_essay_wrapper(prompt, problem_id));
}

var save_essaygrade = function(data) {
    var target_btn = $(data.target);
    var form = target_btn.parent().parent();
    var problem_id = parseInt(form.data("problem_id"))
    var essay_text = form.find('#essay-text').val()
    var api_url = $('#model_name').attr("url") + "/";
    post_data = {
        essay_text : essay_text,
        essay_type : "train",
        problem : problem_id,
        additional_predictors : [],
        has_been_ml_graded : false
    }
    $.ajax({
        type: "POST",
        url: api_url,
        data: { action: "post", model: 'essay', data : JSON.stringify(post_data)}
    }).done(get_courses);
}

$(function(){
    var tokenValue = $.cookie('problemgradercsrftoken');

    $.ajaxSetup({
        data: {csrfmiddlewaretoken: tokenValue },
        headers: {'X-CSRF-Token': tokenValue}
    });
    get_courses()
})