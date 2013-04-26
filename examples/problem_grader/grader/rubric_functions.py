from models import Rubric, RubricOption

def get_rubric_data(problem_id, max_target_scores = None):
    rubric = Rubric.objects.filter(associated_problem=problem_id)
    rubric_dict = []
    if rubric.count>=1:
        rubric = rubric[0]
        rubric_dict = rubric.get_rubric_dict()
    if max_target_scores is not None:
        for i in xrange(0,len(rubric_dict)):
            if max_target_scores[i]==1:
                rubric_dict[i]['selected'] = True
    return rubric_dict

def create_rubric_objects(rubric_data, request):
    rubric = Rubric(associated_problem = rubric_data['problem_id'], user = request.user)
    rubric.save()
    for option in rubric_data['options']:
        option = RubricOption(rubric=rubric, option_points =option['points'], option_text = option['text'])
        option.save()
