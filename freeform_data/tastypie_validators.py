from tastypie.validation import FormValidation
from django.core.exceptions import ImproperlyConfigured
from django.forms import ModelForm
from django.forms.models import model_to_dict
from models import Problem, Essay
import logging
log = logging.getLogger(__name__)

class CustomFormValidation(FormValidation):
    """
    A validation class that uses a Django ``Form`` to validate the data.

    This class **DOES NOT** alter the data sent, only verifies it. If you
    want to alter the data, please use the ``CleanedDataFormValidation`` class
    instead.

    This class requires a ``form_class`` argument, which should be a Django
    ``Form`` (or ``ModelForm``, though ``save`` will never be called) class.
    This form will be used to validate the data in ``bundle.data``.
    """
    def __init__(self, **kwargs):
        for key in ['form_class', 'model_type']:
            if not key in kwargs:
                raise ImproperlyConfigured("You must provide a {0} to 'FormValidation' classes.".format(key))

        self.form_class = kwargs.pop('form_class')
        self.model_type = kwargs.pop('model_type')
        log.debug(self.form_class)
        log.debug(self.model_type)

    def is_valid(self, bundle, request=None):
        """
        Performs a check on ``bundle.data``to ensure it is valid.

        If the form is valid, an empty list (all valid) will be returned. If
        not, a list of errors will be returned.
        """

        form_data, problem_obj = self.form_args(bundle)
        request_path = bundle.request.get_full_path()
        request_model_type = (request_path.split('/')[-3])
        if self.model_type in request_model_type:
            form_data['problem_object'] = problem_obj
        form = self.form_class(**form_data)
        if form.is_valid():
            return {}

        # The data is invalid. Let's collect all the error messages & return
        # them.
        return form.errors

    def uri_to_pk(self, uri):
        """
        Returns the integer PK part of a URI.

        Assumes ``/api/v1/resource/123/`` format. If conversion fails, this just
        returns the URI unmodified.

        Also handles lists of URIs
        """

        if uri is None:
            return None

        # convert everything to lists
        multiple = not isinstance(uri, basestring)
        uris = uri if multiple else [uri]

        # handle all passed URIs
        converted = []
        for one_uri in uris:
            try:
                # hopefully /api/v1/<resource_name>/<pk>/
                converted.append(int(one_uri.split('/')[-2]))
            except (IndexError, ValueError):
                raise ValueError(
                    "URI %s could not be converted to PK integer." % one_uri)

        # convert back to original format
        return converted if multiple else converted[0]

    def form_args(self, bundle):
        kwargs = super(CustomFormValidation, self).form_args(bundle)

        problem_obj = None
        for field in kwargs['data']:
            if field=="problem" and self.model_type=="essay":
                problem_id = self.uri_to_pk(kwargs['data'][field])
                problem_obj = model_to_dict(Problem.objects.get(id=problem_id))
            elif field=="essay" and self.model_type=="essaygrade":
                essay_id = self.uri_to_pk(kwargs['data'][field])
                essay_obj = Essay.objects.get(id=essay_id)
                problem_obj = model_to_dict(essay_obj.problem)

        return kwargs, problem_obj
