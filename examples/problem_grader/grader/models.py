from django.db import models
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

class Rubric(models.Model):
    associated_problem = models.IntegerField()
    user = models.ForeignKey(User)

    def get_total_score(self):
        categories = self.get_rubric_json()
        scores = []
        final_score = 0
        category_set = self.rubriccategory_set.all()
        for category in category_set:
            options = category.rubricoption_set.filter(selected=True)
            if options.count()>0:
                scores.append([options.option_points for option in options])
        if len(scores)>0:
            final_score = sum(scores)

    def get_rubric_json(self):
        categories = []
        category_set = self.rubriccategory_set.all()
        for category in category_set:
            options = category.rubricoption_set.all()
            option_list = []
            for option in options:
                option_list.append(model_to_dict(option))
            category_dict = model_to_dict(category)
            category_dict['options'] = option_list
            categories.append(category_dict)
        return categories

class RubricCategory(models.Model):
    category_name = models.CharField()
    rubric = models.ForeignKey(Rubric)

class RubricOption(models.Model):
    option_points = models.IntegerField()
    option_text = models.TextField()
    selected = models.BooleanField(default=False)
