import slumber
import logging
import requests
import json
import os

log = logging.getLogger(__name__)

def join_without_slash(path1, path2):
    if path1.endswith("/"):
        path1 = path1[0:-1]
    if not path2.startswith("/"):
        path2 = "/" + path2

    return path1 + path2

class InvalidValueException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class SlumberModel(object):
    excluded_fields = ['created', 'id', 'resource_uri', 'id', 'modified']
    def __init__(self,api_url, model_type, api_auth):
        self.api = slumber.API(api_url)
        self.api_url = api_url
        self.model_type = model_type
        self.api_auth = api_auth
        self.objects=[]

    def get_base_model(self, id = None):
        ref = getattr(self.api,self.model_type)
        log.debug(self.api_url)
        if id is not None:
            ref = ref(id)
        return ref

    def get(self, id = None, data = None, **kwargs):
        new_arguments = self.api_auth.copy()
        new_arguments['limit'] = 0
        if id is not None:
            self.objects = self.get_base_model(id).get(**new_arguments)
            return self.objects
        else:
            return self.get_base_model().get(**new_arguments).get('objects', None)

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

    def post(self, id = None, data = None, **kwargs):
        for field in self.required_fields:
            if field not in data:
               error_message = "Key {0} not present in post data, but is required.".format(field)
               log.debug(error_message)
               raise InvalidValueException(error_message)
        new_arguments = self.api_auth.copy()
        new_arguments['data'] = data
        new = self.get_base_model().post(**new_arguments)
        self.objects.append(new)
        return new

    def find_model_by_id(self,id):
        match = None
        for i in xrange(0,len(self.objects)):
            loop_obj = self.objects[i]
            if int(loop_obj['id']) == id:
                match = i
                break
        return match

    def delete(self,id = None, data = None, **kwargs):
        response = self.get_base_model(id=id).delete(**self.api_auth)
        match = self.find_model_by_id(id)
        if match is not None:
            self.objects.pop(match)
        return response

    def update(self, id = None, data = None, **kwargs):
        self.get()
        new_arguments = self.api_auth.copy()
        new_arguments['data'] = data
        response = self.get_base_model(id=id).update(**new_arguments)
        match = self.find_model_by_id(id)
        self.objects[match] = response
        return response

    def action(self, action, id=None, data = None):
        action_dict = {
            'get' : self.get,
            'post' : self.post,
            'update' : self.update,
            'delete' : self.delete,
        }
        if action not in action_dict:
            error = "Could not find action {0} in registered actions.".format(action)
            log.info(error)
            raise InvalidValueException(error)

        if action in ['update', 'delete'] and id is None:
            error = "Need to provide an id along with action {0}.".format(action)
            log.info(error)
            raise InvalidValueException(error)

        if action in ['update', 'post'] and data is None:
            error = "Need to provide data along with action {0}.".format(action)
            log.info(error)
            raise InvalidValueException(error)

        result = action_dict[action](data=data, id=id)
        return result

class SlumberModelDiscovery(object):
    def __init__(self,api_url, api_auth):
        self.api_url = api_url
        self.api_auth = api_auth
        self.schema_url = join_without_slash(self.api_url, "?format=json")

    def get_schema(self):
        schema = requests.get(self.schema_url, params=self.api_auth)
        return json.loads(schema.content)

    def generate_models(self, model_names = None):
        schema = self.get_schema()
        slumber_models = {}
        for field in schema:
            if model_names is not None and field not in model_names:
                continue
            field_model = SlumberModel(self.api_url, field, self.api_auth)
            slumber_models[field] = field_model
        return slumber_models



