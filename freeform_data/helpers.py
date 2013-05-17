from django.contrib.contenttypes.models import ContentType
from guardian.models import UserObjectPermission
from django.contrib.auth.models import Permission

def get_content_id(model):
    content_type = ContentType.objects.get_for_model(model)
    return content_type.id, content_type.name

def get_object_permissions(instance, model):
    content_id, content_name = get_content_id(model)
    permissions = UserObjectPermission.objects.filter(content_type=content_id, object_pk = instance.id)
    return permissions

def copy_permissions(base_instance, base_model, new_instance, new_model):
    base_permissions = get_object_permissions(base_instance, base_model)
    new_content_id, new_content_name = get_content_id(new_model)
    for permission in  base_permissions:
        permission.pk = None
        permission.id = None
        permission.content_type = new_content_id
        permission.object_pk = new_instance.id
        new_permission_name = generate_new_permission(permission.permission.codename, new_content_name)
        django_permission = Permission.objects.get(codename=new_permission_name)
        permission.permission = django_permission
        permission.save()

def generate_new_permission(permission_name, new_model_name):
    permission_list = permission_name.split("_")
    permission_list = permission_list[0:(len(permission_list)-1)]
    permission_list += [new_model_name]
    new_permission = "_".join(permission_list)
    return new_permission