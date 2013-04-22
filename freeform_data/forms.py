from django import forms
import fields
import django_validators
import logging
from django.forms.fields import Field, FileField
from django.core.exceptions import ValidationError

log = logging.getLogger(__name__)

class ProblemForm(forms.Form):
    def __init__(self, problem_object= None, **kwargs):
        super(ProblemForm, self).__init__(**kwargs)
        validator = django_validators.JSONListValidator()
        self.fields['max_target_scores'] = fields.JSONListField(required=True, validators=[validator])

class EssayForm(forms.Form):
    def __init__(self, problem_object=None, **kwargs):
        super(EssayForm, self).__init__(**kwargs)
        if problem_object is not None:
            self.add_pred_length = problem_object.get('number_of_additional_predictors',0)
        else:
            self.add_pred_length = 0

        validator = django_validators.JSONListValidator(matching_list_len=self.add_pred_length)

        self.fields['additional_predictors'] = fields.JSONListField(required = False, validators=[validator])

class EssayGradeForm(forms.Form):
    def __init__(self, problem_object = None, **kwargs):
        super(EssayGradeForm, self).__init__(**kwargs)
        self.max_target_scores = None
        if problem_object is not None:
            self.max_target_scores = problem_object.get('max_target_scores',None)

        validator = django_validators.JSONListValidator(matching_list=self.max_target_scores)

        self.fields['target_scores'] = fields.JSONListField(required = True, validators=[validator])