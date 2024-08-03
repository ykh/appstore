from appstore.utils.permission import permission
from users.models import User


@permission
def has_create_permission(user: User):
    return user.is_authenticated


@permission
def has_retrieve_permission(user: User):
    return user.is_authenticated


@permission
def has_list_permission(user: User):
    return user.is_authenticated


@permission
def has_update_permission(app_user_id: str, user: User):
    if user.is_anonymous:
        return False

    if user.is_superuser or user.is_staff:
        return True

    return app_user_id == user.id


@permission
def has_destroy_permission(app_user_id: str, user: User):
    if user.is_anonymous:
        return False

    if user.is_superuser or user.is_staff:
        return True

    return app_user_id == user.id
