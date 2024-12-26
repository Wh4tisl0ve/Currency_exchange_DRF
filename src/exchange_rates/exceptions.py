from rest_framework.exceptions import APIException
from rest_framework import status


class ConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Валютная пара с таким кодом уже существует"
