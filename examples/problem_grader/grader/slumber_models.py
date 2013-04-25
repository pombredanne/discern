import slumber

class SlumberModel(object):
    def __init__(self,api_url, model_type, api_auth):
        self.api = slumber.API(api_url)
        self.model_type = model_type
        self.api_auth = api_auth
        self.objects = []

    def get_base_model(self, id = None):
        ref = getattr(self.api,self.model_type)
        if id is not None:
            ref = ref(id)
        return ref

    def get(self):
        self.objects = self.get_base_model().get(**self.api_auth)['objects']
        return self.objects

    def schema(self):
        schema = self.get_base_model().schema.get(**self.api_auth)['fields']
        return schema

    def get_required_fields(self):
        schema = self.schema()
        required_fields = []
        for field in schema:
            if not schema['field']['nullable']:
                required_fields.append(field)
        return required_fields
    
    def post(self, post_data):
        pass