import datetime
from haystack import indexes
from haystack import site
from models import Organization, Course, Problem, Essay, EssayGrade

class BaseIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    model_type = None

    def get_model(self):
        return self.model_type

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class OrganizationIndex(BaseIndex):
    model_type = Organization

class CourseIndex(BaseIndex):
    model_type = Course

class ProblemIndex(BaseIndex):
    model_type = Problem

class EssayIndex(BaseIndex):
    model_type = Essay

class EssayGradeIndex(BaseIndex):
    model_type = EssayGrade

site.register(Organization, OrganizationIndex)
site.register(Course, CourseIndex)
site.register(Problem, ProblemIndex)
site.register(Essay, EssayIndex)
site.register(EssayGrade, EssayGradeIndex)