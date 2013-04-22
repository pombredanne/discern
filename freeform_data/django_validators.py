import json
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _, ungettext_lazy

class JSONListValidator(object):
    message = _('Invalid Json List.')

    def __init__(self, matching_list=None, message=None, matching_list_len = None):
        self.matching_list = matching_list
        if message is not None:
            self.message = message

        if self.matching_list is not None:
            try:
                self.matching_list = json.loads(self.matching_list)
            except Exception:
                pass

            self.matching_list_len = len(self.matching_list)

    def __call__(self, value):
        """
        Validates that the input matches the regular expression.
        """
        try:
            value = json.loads(value)
        except Exception:
            pass

        value_len = len(value)

        if not isinstance(value,list):
            raise ValidationError(self.message)

        if self.matching_list_len is not None:
            if self.matching_list_len!=value_len:
                raise ValidationError(self.message)

        if self.matching_list is not None:
            for i in xrange(0,self.matching_list_len):
                if value[i]>self.matching_list[i]:
                    raise ValidationError(self.message)



