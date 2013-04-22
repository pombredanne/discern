from django import forms
import fields
import django_validators

class ProblemForm(forms.Form):
    def __init__(self, problem_object = None, **kwargs):
        super(ProblemForm, self).__init__()

    max_target_scores = fields.JSONListField(required=True)

class EssayForm(forms.Form):
    def __init__(self, problem_object = None, **kwargs):
        if problem_object is not None:
            self.add_pred_length = problem_object.get('number_of_additional_predictors',0)
        else:
            self.add_pred_length = 0

        super(EssayForm, self).__init__()

        validator = django_validators.JSONListValidator(matching_list_len=self.add_pred_length)

        self.additional_predictors = fields.JSONListField(required = False, validators=[validator])

class EssayGradeForm(forms.Form):
    def __init__(self, problem_object = None, **kwargs):
        self.max_target_scores = None
        if problem_object is not None:
            self.max_target_scores = problem_object.get('max_target_scores',None)

        super(EssayGradeForm, self).__init__()

        validator = django_validators.JSONListValidator(matching_list=self.max_target_scores)

        self.target_scores = fields.JSONListField(required = True, validators=[validator])