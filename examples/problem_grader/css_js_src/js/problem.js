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
    var problems = new Array();
    for (var i = 0; i < data.length; i++) {
        var elem = data[i];
        var mod_problem_name = elem.name.replace(" ", "_");

        var elem_dict = {
            name : elem.name,
            href : elem.id + mod_problem_name,
            user_count : elem.users.length,
            problem_count: elem.problems.length,
            modified : new Date(Date.parse(elem.modified)),
            created: new Date(Date.parse(elem.created)),
            id : elem.id
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
}

var add_rubric_option = function(target) {
    var target_btn = $(target.target);
    var rubric_container = target_btn.parent();
    rubric_container.prepend()
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
    var inputs = form.find('input')
    var problem_name = inputs.val()
    var api_url = $('#model_name').attr("url") + "/";
    post_data = {
        problem_name : problem_name
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