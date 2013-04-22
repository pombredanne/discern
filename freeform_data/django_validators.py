import json
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _, ungettext_lazy
import logging
log = logging.getLogger(__name__)

class JSONListValidator(object):
    message = _('Invalid Json List.')

    def __init__(self, matching_list=None, message=None, matching_list_len = None):
        self.matching_list = matching_list
        self.matching_list_len = None
        if message is not None:
            self.message = message

        if matching_list_len is not None and isinstance(matching_list_len, int):
            self.matching_list_len = matching_list_len

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

        if not isinstance(value,list):
            error_message = "You entered a non-list entry for value, or entered bad json. {0}".format(value)
            raise ValidationError(error_message)

        value_len = len(value)

        for val in value:
            if not isinstance(val,int):
                error_message="You entered a non-integer value in your score list. {0}".format(value)
                raise ValidationError(error_message)

        if self.matching_list_len is not None:
            if self.matching_list_len!=value_len:
                error_message = "You entered more target scores than exist in the corresponding maximum list in the problem.  {0} vs {1}".format(value_len, self.matching_list_len)
                raise ValidationError(error_message)

        if self.matching_list is not None:
            for i in xrange(0,self.matching_list_len):
                if value[i]>self.matching_list[i]:
                    error_message = "Value {i} in provided scores greater than max defined in problem. {value} : {matching}".format(i=i, value=value, matching=self.matching_list)
                    raise ValidationError(error_message)



