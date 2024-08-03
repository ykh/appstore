from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def base_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, exceptions.ValidationError):
            custom_response_data = {
                'type': exceptions.ValidationError.__name__,
                'message': response.data,
                'code': response.status_code,
            }
        else:
            custom_response_data = {
                'type': exc.__class__.__name__,
                'message': response.data.get('detail', str(exc)),
                'code': response.status_code,
            }

        response.data = custom_response_data
    else:
        custom_response_data = {
            'type': exceptions.APIException.__name__,
            'message': 'An unexpected error occurred.',
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        }

        response = Response(
            custom_response_data,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
