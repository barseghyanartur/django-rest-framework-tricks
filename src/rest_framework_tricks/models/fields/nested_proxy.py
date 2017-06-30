"""
Fields.
"""

from ...utils import DictProxy

__title__ = 'rest_framework_tricks.models.fields.nested_proxy'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'NestedProxyField',
)


def NestedProxyField(*fields, **options):
    """NestedProxyField field.

    Example:

        >>> from django.db import models
        >>> from rest_framework_tricks.models.fields import NestedProxyField
        >>> from .constants import BOOK_STATUS_CHOICES, BOOK_STATUS_DEFAULT
        >>>
        >>>
        >>> class Book(models.Model):
        >>>
        >>>     title = models.CharField(max_length=100)
        >>>     description = models.TextField(null=True, blank=True)
        >>>     summary = models.TextField(null=True, blank=True)
        >>>     publication_date = models.DateField()
        >>>     state = models.CharField(max_length=100,
        >>>                              choices=BOOK_STATUS_CHOICES,
        >>>                              default=BOOK_STATUS_DEFAULT)
        >>>     isbn = models.CharField(max_length=100, unique=True)
        >>>     price = models.DecimalField(max_digits=10, decimal_places=2)
        >>>     pages = models.PositiveIntegerField(default=200)
        >>>     stock_count = models.PositiveIntegerField(default=30)
        >>>
        >>>     # This does not cause a model change
        >>>     publishing_information = NestedProxyField(
        >>>         'publication_date',
        >>>         'isbn',
        >>>         'pages',
        >>>     )
        >>>
        >>>     # This does not cause a model change
        >>>     stock_information = NestedProxyField(
        >>>         'stock_count',
        >>>         'price',
        >>>         'state',
        >>>     )
        >>>
        >>>     class Meta(object):
        >>>
        >>>         ordering = ["isbn"]
        >>>
        >>>     def __str__(self):
        >>>         return self.title
    """

    __as_object = options.get('as_object', False)

    @property
    def proxy_field(self):
        __dict = {}
        for __field in fields:
            if hasattr(self, __field):
                __dict.update({__field: getattr(self, __field)})
        if __as_object is True:
            return DictProxy(__dict)
        return __dict

    return proxy_field
