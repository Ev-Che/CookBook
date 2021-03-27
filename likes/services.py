from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from .models import Like

User = get_user_model()


def add_like(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    _, is_created = Like.objects.get_or_create(content_type=obj_type,
                                               object_id=obj.id,
                                               user=user)
    return True


def remove_like(obj, user):
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(content_type=obj_type,
                        object_id=obj.id, user=user).delete()
    return not Like.objects.filter(content_type=obj_type,
                                   object_id=obj.id, user=user).exists()


def is_fan(obj, user):
    if user.is_authenticated:
        obj_type = ContentType.objects.get_for_model(obj)
        likes = Like.objects.filter(content_type=obj_type,
                                    object_id=obj.id, user=user)
        return likes.exists()
    return False
