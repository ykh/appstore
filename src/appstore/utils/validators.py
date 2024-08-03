from functools import wraps
from uuid import UUID


def validate_uuid(param_name, exception, message, is_optional=False):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            param_value = kwargs.get(param_name)

            if is_optional and param_value is None:
                return fn(*args, **kwargs)

            if isinstance(param_value, UUID):
                return fn(*args, **kwargs)

            if not isinstance(param_value, str):
                raise exception(message)

            try:
                UUID(param_value)
            except (ValueError, AttributeError):
                raise exception(message)

            return fn(*args, **kwargs)

        return wrapper

    return decorator
