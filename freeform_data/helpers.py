from django.contrib.contenttypes.models import ContentType
from guardian.models import UserObjectPermission
from django.contrib.auth.models import Permission

def get_content_id(model):
    content_type = ContentType.objects.get_for_model(model)
    return content_type.id, content_type.name

def get_object_permissions(instance, model):
    content_id = get_content_id(model)
    permissions = UserObjectPermission.objects.filter(content_type=content_id, object_pk = instance.id)
    return permissions

def copy_permissions(base_instance, base_model, new_instance, new_model):
    base_permissions = get_object_permissions(base_instance, base_model)
    new_content_id = get_content_id(new_model)
    for permission in  base_permissions:
        permission.pk = None
        permission.id = None
        permission.content_type = new_content_id
        permission.object_pk = new_instance.id