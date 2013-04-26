var get_models = function(api_url, model_type, callback) {
    $.ajax({
        type: "GET",
        url: api_url,
        data: { action: "get", model: model_type }
    }).done(callback);
}

var render_problem = function(data) {
    var model_data = $("#model_container");
    model_data.empty();
    data = $.parseJSON(data);
    var item_template = $( "#problem-item-template" ).html();
    var container_template = $( "#problem-list-template" ).html();
    var rubric_list_template = $('#rubric-list-template').html();

    var problems = new Array();
    for (var i = 0; i < data.length; i++) {
        var elem = data[i];
        var mod_problem_name = elem.name.replace(" ", "_");
        console.log(elem.rubric)

        var elem_dict = {
            name : elem.name,
            prompt : elem.prompt,
            href : elem.id + mod_problem_name,
            modified : new Date(Date.parse(elem.modified)),
            created: new Date(Date.parse(elem.created)),
            id : elem.id,
            rubric : _.template(rubric_list_template,{rubrics : elem.rubric})
        }
        problems.push(_.template(item_template,elem_dict));
    }
    var template_data = {
        problems: problems
    };
    model_data.append(_.template(container_template,template_data))
    add_problem_button()
    $('#create-problem').click(create_problem);
    $('.delete-problem').click(delete_problem);
    $('#rubricadd').click(add_rubric_option);
}

var add_rubric_option = function(target) {
    var target_btn = $(target.target);
    var rubric_container = target_btn.parent().find('#rubric-item-container');
    rubric_container.find(".rubric_input").attr('disabled','disabled');
    var rubric_template = $( "#rubric-item-template" ).html();
    var rubric_dict = {
        finished : false
    }
    var rubric_html = _.template(rubric_template,rubric_dict)
    rubric_container.append(rubric_html)
}

var add_problem_button = function() {
    var model_add = $("#model_add")
    model_add.empty()
    var add_template = $( "#problem-add-template" ).html();
    var rubric_template = $( "#rubric-item-template" ).html();
    var rubric_dict = {
        finished : false
    }
    var rubric_html = _.template(rubric_template,rubric_dict)
    var add_dict = {
        name : "Add a problem",
        href: "problem-add",
        rubric: rubric_html
    }
    model_add.html(_.template(add_template,add_dict))
}

var get_problem_items = function(model_type) {
    var api_base = $('#model_name').attr("url");
    switch(model_type)
    {
        case "problem":
            callback = render_problem;
            break;
    }
    get_models(api_base, model_type, callback)
}

var delete_problem = function(target) {
    var target_btn = $(target.target);
    var data = target_btn.parent();
    console.log(data)
    var id = data.data('elem_id')
    var api_url = $('#model_name').attr("url") + "/";
    $.ajax({
        type: "POST",
        url: api_url,
        data: { action: "delete", model: 'problem', id : id}
    }).done(get_model_type_and_items);
}

var create_problem = function(target) {
    var target_btn = $(target.target);
    var form = target_btn.parent().parent().parent();
    var problem_name = form.find('#problem-name-input').val()
    var prompt = form.find('#promptname').val()
    var rubric = form.find("#rubric-item-container")
    var rubric_items = rubric.find(".rubric-item")
    options = new Array();
    var course = $("#model_name").data("course_id")
    for (var i=0 ; i < rubric_items.length ; i++) {
        options.push({
            points: rubric_items.eq(i).find('select').find(":selected").text(),
            text : rubric_items.eq(i).find('textarea').val()
        })
    }
    var rubric = {
        options : options
    }
    var api_url = $('#model_name').attr("url") + "/";
    post_data = {
        name : problem_name,
        prompt : prompt,
        rubric : rubric,
        course : course
    }
    $.ajax({
        type: "POST",
        url: api_url,
        data: { action: "post", model: 'problem', data : JSON.stringify(post_data)}
    }).done(get_model_type_and_items);
}

var get_model_type_and_items = function() {
    var model_type = $('#model_name').attr('model');
    if(model_type!=undefined) {
        get_problem_items(model_type)
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