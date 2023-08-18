from rest_framework import status
from rest_framework.exceptions import APIException


class BaseAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail):
        self.detail = {"message": detail, "success": False}


class BadRequestException(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST


class NotFoundException(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND


class SomethingWentWrongException(BaseAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class ForbiddenException(BadRequestException):
    status_code = status.HTTP_403_FORBIDDEN


class UnValidSerializerException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, details):
        self.detail = {**details, "success": False}
