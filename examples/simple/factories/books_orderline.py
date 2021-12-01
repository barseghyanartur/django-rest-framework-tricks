"""
Books OrderLine model factory.
"""

from factory import SubFactory
from factory.django import DjangoModelFactory

from books.models import OrderLine

# from .factory_faker import Faker

__all__ = ("OrderLineFactory",)


class OrderLineFactory(DjangoModelFactory):
    """Order line factory."""

    # owner = SubFactory('factories.books_order.OrderFactory')
    book = SubFactory("factories.books_book.BookFactory")
    # created = Faker('date')
    # updated = Faker('date')

    class Meta:
        """Meta class."""

        model = OrderLine
