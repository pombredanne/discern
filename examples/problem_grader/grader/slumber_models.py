import slumber
import logging
log = logging.getLogger(__name__)

class SlumberModel(object):
    excluded_fields = ['created', 'id', 'resource_uri', 'id', 'modified']
    def __init__(self,api_url, model_type, api_auth):
        self.api = slumber.API(api_url)
        self.model_type = model_type
        self.api_auth = api_auth
        self.get()

    def get_base_model(self, id = None):
        ref = getattr(self.api,self.model_type)
        if id is not None:
            ref = ref(id)
        return ref

    def get(self):
        new_arguments = self.api_auth.copy()
        new_arguments['limit'] = 0
        self.objects = self.get_base_model().get(**new_arguments).get('objects', None)
        return self.objects

    @property
    def schema(self):
        schema = self.get_base_model().schema.get(**self.api_auth).get('fields', None)
        return schema

    @property
    def required_fields(self):
        schema = self.schema
        required_fields = []
        for field in schema:
            if (not schema[field]['nullable'] or schema[field]['blank']) and field not in self.excluded_fields:
                required_fields.append(field)
        return required_fields

    def post(self, post_data):
        for field in self.required_fields:
            if field not in post_data:
               error_message = "Key {0} not present in post data, but is required.".format(field)
               log.debug(error_message)
               return False, error_message
        new_arguments = self.api_auth.copy()
        new_arguments['data'] = post_data
        new = self.get_base_model().post(**new_arguments)
        self.objects.append(new)
        return True, new

    def find_model_by_id(self,id):
        match = None
        for i in xrange(0,len(self.objects)):
            loop_obj = self.objects[i]
            if int(loop_obj['id']) == id:
                match = i
                break
        return match

    def delete(self,id):
        response = self.get_base_model(id=id).delete(**self.api_auth)
        match = self.find_model_by_id(id)
        if match is not None:
            self.objects.pop(match)
        return response

    def update(self, id, update_data):
        new_arguments = self.api_auth.copy()
        new_arguments['data'] = update_data
        response = self.get_base_model(id=id).update(**new_arguments)
        match = self.find_model_by_id(id)
        self.objects[match] = response
        return response

