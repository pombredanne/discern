from django.db import models
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

class Rubric(models.Model):
    associated_problem = models.IntegerField()
    user = models.ForeignKey(User)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_scores(self):
        scores = []
        all_scores = []
        final_score=0
        max_score = 0
        options = self.get_rubric_dict()
        for option in options:
            all_scores.append(option['option_points'])
            if option['selected']:
                scores.append(option['option_points'])

        if len(scores)>0:
            final_score = sum(scores)

        if len(all_scores)>0:
            max_score = sum(all_scores)

        return {
            'score' : final_score,
            'max_score' : max_score
        }

    def get_rubric_dict(self):
        options = []
        option_set = self.rubricoption_set.all().order_by('id')
        for option in option_set:
            options.append(model_to_dict(option))
        return options

class RubricOption(models.Model):
    rubric = models.ForeignKey(Rubric)
    option_points = models.IntegerField()
    option_text = models.TextField()
    selected = models.BooleanField(default=False)
