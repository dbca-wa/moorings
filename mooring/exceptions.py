
import logging

from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework import serializers
from rest_framework.exceptions import APIException, NotAuthenticated, PermissionDenied
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


class BookingRangeWithinException(Exception):
    pass


class InternalServerError(APIException):
    status_code = 500
    default_detail = "A server error occurred."
    default_code = "internal_server_error"
    

def custom_exception_handler(exc, context):
    """Custom django rest framework exception handler
    That makes sure all the exception responses are in json format since many django
    exceptions are in html format
    """

    # Django rest framework errors are already in json format
    if isinstance(
        exc, (serializers.ValidationError, Http404, NotAuthenticated, PermissionDenied)
    ):
        pass

    # handle django validation errors
    elif isinstance(exc, ValidationError):
        if hasattr(exc, "error_dict"):
            exc = serializers.ValidationError(repr(exc.error_dict))
        elif hasattr(exc, "message"):
            exc = serializers.ValidationError(exc.message)
        else:
            exc = serializers.ValidationError(str(exc))

    else:
        # Handle all other exceptions
        logger.exception(str(exc))
        exc = InternalServerError(str(exc))

    return exception_handler(exc, context)