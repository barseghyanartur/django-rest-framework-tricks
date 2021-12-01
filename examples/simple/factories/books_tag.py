"""
Books Tag model factory.
"""

import random

from factory import LazyAttribute
from factory.django import DjangoModelFactory

from books.models import Tag

from .factory_faker import Faker

__all__ = (
    "TagFactory",
    "LimitedTagFactory",
)


class BaseTagFactory(DjangoModelFactory):
    """Base tag factory."""

    # Although the ``max_length`` of the of the ``title`` field of the
    # ``Tag`` model is set to 255, for usability we set this one to 20.
    title = Faker("catch_phrase")

    class Meta:
        """Meta class."""

        model = Tag
        abstract = True
        django_get_or_create = ("title",)


class TagFactory(BaseTagFactory):
    """Tag factory."""


class LimitedTagFactory(BaseTagFactory):
    """Tag factory, but limited to 20 tags."""

    id = LazyAttribute(lambda __x: random.randint(1, 20))

    class Meta:
        """Meta class."""

        django_get_or_create = ("id",)
