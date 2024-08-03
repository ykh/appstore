from rest_framework.exceptions import PermissionDenied


def permission(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)

        if not result:
            message = f'Permission denied on {fn.__name__}.'

            raise PermissionDenied(message)
        return result

    return wrapper
