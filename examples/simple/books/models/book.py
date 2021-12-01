"""
Book model.
"""

from django.db import models
from rest_framework_tricks.models.fields import NestedProxyField

from ..constants import (
    BOOK_PUBLISHING_STATUS_CHOICES,
    BOOK_PUBLISHING_STATUS_DEFAULT,
)

__all__ = (
    'Book',
    'BookProxy',
    'BookProxy2',
)


class Book(models.Model):
    """Book."""

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField('books.Author', related_name='books')
    publisher = models.ForeignKey('books.Publisher',
                                  related_name='books',
                                  null=True,
                                  blank=True,
                                  on_delete=models.CASCADE)
    publication_date = models.DateField()
    state = models.CharField(max_length=100,
                             choices=BOOK_PUBLISHING_STATUS_CHOICES,
                             default=BOOK_PUBLISHING_STATUS_DEFAULT)
    isbn = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pages = models.PositiveIntegerField(default=200)
    stock_count = models.PositiveIntegerField(default=30)
    tags = models.ManyToManyField('books.Tag',
                                  related_name='books',
                                  blank=True)

    # This does not cause a model change
    publishing_information = NestedProxyField(
        'publication_date',
        'isbn',
        'pages',
    )

    # This does not cause a model change
    stock_information = NestedProxyField(
        'stock_count',
        'price',
        'state',
    )

    class Meta:
        """Meta options."""

        ordering = ["isbn"]

    def __str__(self):
        return self.title


class BookProxy(Book):
    """Book proxy model for to be used in testing."""

    class Meta:
        """Meta options."""

        proxy = True


class BookProxy2(Book):
    """Book proxy model for to be used in testing."""

    class Meta:
        """Meta options."""

        proxy = True
