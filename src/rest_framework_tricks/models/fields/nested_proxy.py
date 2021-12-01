"""
Nested proxy field.
"""

from ...utils import DictProxy

__title__ = "rest_framework_tricks.models.fields.nested_proxy"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2017-2019 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = ("NestedProxyField",)


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
        >>>     class Meta:
        >>>
        >>>         ordering = ["isbn"]
        >>>
        >>>     def __str__(self):
        >>>         return self.title

    Nesting depth is unlimited, so the following would be possible as well.

    Example:

        >>> class Author(models.Model):
        >>>
        >>>     salutation = models.CharField(max_length=10)
        >>>     name = models.CharField(max_length=200)
        >>>     email = models.EmailField()
        >>>     birth_date = models.DateField(null=True, blank=True)
        >>>     biography = models.TextField(null=True, blank=True)
        >>>     phone_number = models.CharField(max_length=200,
        >>>                                     null=True,
        >>>                                     blank=True)
        >>>     website = models.URLField(null=True, blank=True)
        >>>     company = models.CharField(max_length=200,
        >>>                                null=True,
        >>>                                blank=True)
        >>>     company_phone_number = models.CharField(max_length=200,
        >>>                                             null=True,
        >>>                                             blank=True)
        >>>     company_email = models.EmailField(null=True, blank=True)
        >>>     company_website = models.URLField(null=True, blank=True)
        >>>
        >>>     # This does not cause a model change
        >>>     personal_contact_information = NestedProxyField(
        >>>         'email',
        >>>         'phone_number',
        >>>         'website',
        >>>     )
        >>>
        >>>     # This does not cause a model change
        >>>     business_contact_information = NestedProxyField(
        >>>         'company',
        >>>         'company_email',
        >>>         'company_phone_number',
        >>>         'company_website',
        >>>     )
        >>>
        >>>     # This does not cause a model change
        >>>     contact_information = NestedProxyField(
        >>>         'personal_contact_information',
        >>>         'business_contact_information',
        >>>     )

    You could even do this (although the way it's written above is at the
    moment the preferred/recommended way of dealing with unlimited nesting
    depth.

        >>>     # This does not cause a model change
        >>>     contact_information = NestedProxyField(
        >>>         {
        >>>             'personal_contact_information': (
        >>>                 'email',
        >>>                 'phone_number',
        >>>                 'website',
        >>>             )
        >>>         },
        >>>         {
        >>>             'business_contact_information': (
        >>>                 'company',
        >>>                 'company_email',
        >>>                 'company_phone_number',
        >>>                 'company_website',
        >>>             )
        >>>         },
        >>>     )
    """

    __as_object = options.get("as_object", False)

    @property
    def proxy_field(self):
        """Proxy field."""
        obj = options.get("obj") if "obj" in options else self
        __dict = {}
        for __field in fields:
            # If dictionary
            if isinstance(__field, dict):
                for __key, __values in __field.items():
                    setattr(obj.__class__, __key, NestedProxyField(*__values, obj=obj))
                    __dict.update({__key: getattr(obj, __key)})
            # If string
            else:
                if hasattr(self, __field):
                    __dict.update({__field: getattr(obj, __field)})
        if __as_object is True:
            return DictProxy(__dict)
        return __dict

    return proxy_field
