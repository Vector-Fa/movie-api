from typing import TypeVar, Any, Type

from django.db import models

from .exceptions import NotFoundException, UnValidSerializerException


T = TypeVar('T', bound=models.Model)


def get_or_404(klass: Type[T], **kwargs: Any) -> T:
    try:
        return klass.objects.get(**kwargs)
    except klass.DoesNotExist:
        raise NotFoundException(f'{klass.__name__} not found')


def is_serializer_valid(serializer) -> None:
    if not serializer.is_valid():
        raise UnValidSerializerException(serializer.errors)
