var toggle_grading_container = function(target) {
    var target = $(target.target);
    var container = target.parent();
    var grading_container = container.find(".grading-container");
    if(grading_container.is(":visible")) {
        grading_container.hide();
    } else {
        grading_container.show();
    }

}

var render_essay_wrapper = function(prompt, problem_id) {
    var render_essay = function(data) {
        var model_data = $("#essay-container");
        model_data.empty();
        data = $.parseJSON(data);
        var item_template = $( "#essay-item-template" ).html();
        var container_template = $( "#essay-list-template" ).html();
        var rubric_list_template = $('#rubric-list-template').html();
        var essaygrades_template = $('#essay-grades-template').html();
        var essaygrade_tab_template = $('#essay-grade-tab-template').html();
        var essaygrade_detail_template = $('#essay-grade-detail-template').html();

        var essays = new Array();

        for (var i = 0; i < data.length; i++) {
            var essaygrade_tabs = new Array();
            var essaygrade_details = new Array();
            var elem = data[i];
            var essay_name = "Essay with id " + elem.id.toString();
            var mod_essay_name = essay_name.replace(/ /g, "_");
            var essaygrade_data = elem.essaygrades_full
            for (var z = 0; z < essaygrade_data.length; z++) {
                essaygrade_rubric = essaygrade_data[z]['rubric']
                essaygrade_href = "Essaygrade with id" + essaygrade_data[z]['id']
                essaygrade_href = essaygrade_href.replace(/ /g, "_");
                essaygrade_type = essaygrade_data[z].grader_type;
                var essaygrade_dict = {
                    href : essaygrade_href,
                    rubrics : essaygrade_rubric,
                    type : essaygrade_type
                }
                var essaygrade_tab = _.template(essaygrade_tab_template,essaygrade_dict);
                var essaygrade_detail = _.template(essaygrade_detail_template,essaygrade_dict);
                essaygrade_tabs.push(essaygrade_tab);
                essaygrade_details.push(essaygrade_detail);
            }
            var essaygrades_html = _.template(essaygrades_template,{tabs : essaygrade_tabs, details : essaygrade_details});
            var elem_dict = {
                name : essay_name,
                prompt : prompt,
                href : mod_essay_name,
                modified : new Date(Date.parse(elem.modified)),
                created: new Date(Date.parse(elem.created)),
                id : elem.id,
                essay_text : elem.essay_text,
                rubric : _.template(rubric_list_template,{rubrics : elem.rubric}),
                essaygrades : essaygrades_html
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
        model_data.append(_.template(container_template,template_data));
        var grading_container = $('.grading-container');
        grading_container.hide();
        $('.grade-essay').click(toggle_grading_container);
        $('.create-essaygrade').click(save_essaygrade);
    }
    return render_essay
}

var get_essay_template = function(data) {
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
    var grading_container = target_btn.parent().parent();
    var feedback = grading_container.find('.essay-feedback').val()
    var rubric_scores = new Array();
    var rubric_item_selects = grading_container.find('.rubric-item-select')
    var essay_id = grading_container.parent().parent().parent().find('.accordion-toggle').data('elem_id')
    for(var i=0;i < rubric_item_selects.length ; i++) {
        var item_score = 0
        if($(rubric_item_selects[i]).is(':checked')) {
            item_score = 1
        }
        rubric_scores.push(item_score)
    }
    var api_url = $('#model_name').attr("url") + "/";
    post_data = {
        target_scores: JSON.stringify(rubric_scores),
        essay : essay_id,
        confidence : 1,
        feedback: feedback,
        success: true,
        grader_type: "IN",
        premium_feedback_scores: JSON.stringify("[]"),
        annotated_text: ""
    }
    $.ajax({
        type: "POST",
        url: api_url,
        data: { action: "post", model: 'essaygrade', data : JSON.stringify(post_data)}
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