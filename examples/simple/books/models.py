"""
Models.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from rest_framework_tricks.models.fields import NestedProxyField

from six import python_2_unicode_compatible

from .constants import (
    BOOK_PUBLISHING_STATUS_CHOICES,
    BOOK_PUBLISHING_STATUS_DEFAULT,
)

__all__ = (
    'Author',
    'AuthorProxy',
    'Book',
    'Order',
    'OrderLine',
    'Publisher',
    'Profile',
    'Tag',
)


@python_2_unicode_compatible
class Publisher(models.Model):
    """Publisher."""

    name = models.CharField(max_length=30)
    info = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state_province = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField()

    # This does not cause a model change
    address_information = NestedProxyField(
        'address',
        'city',
        'state_province',
        'country',
        as_object=True
    )

    class Meta(object):
        """Meta options."""

        ordering = ["id"]

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Author(models.Model):
    """Author."""

    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='authors', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    company_phone_number = models.CharField(max_length=200,
                                            null=True,
                                            blank=True)
    company_email = models.EmailField(null=True, blank=True)
    company_website = models.URLField(null=True, blank=True)

    # # This does not cause a model change
    # personal_contact_information = NestedProxyField(
    #     'email',
    #     'phone_number',
    #     'website',
    # )
    #
    # # This does not cause a model change
    # business_contact_information = NestedProxyField(
    #     'company',
    #     'company_email',
    #     'company_phone_number',
    #     'company_website',
    # )
    #
    # # This does not cause a model change
    # contact_information = NestedProxyField(
    #     'personal_contact_information',
    #     'business_contact_information',
    # )

    # This does not cause a model change
    contact_information = NestedProxyField(
        {
            'personal_contact_information': (
                'email',
                'phone_number',
                'website',
            )
        },
        {
            'business_contact_information': (
                'company',
                'company_email',
                'company_phone_number',
                'company_website',
            )
        },
    )

    class Meta(object):
        """Meta options."""

        ordering = ["id"]

    def __str__(self):
        return self.name


class AuthorProxy(Author):
    """Author proxy model for to be used in testing."""

    # This does not cause a model change
    personal_contact_information = NestedProxyField(
        'email',
        'phone_number',
        'website',
    )

    # This does not cause a model change
    business_contact_information = NestedProxyField(
        'company',
        'company_email',
        'company_phone_number',
        'company_website',
    )

    # This does not cause a model change
    contact_information = NestedProxyField(
        'personal_contact_information',
        'business_contact_information',
    )

    class Meta(object):
        """Meta options."""

        proxy = True


class Tag(models.Model):
    """Simple tag model."""

    title = models.CharField(max_length=255, unique=True)

    class Meta(object):
        """Meta options."""

        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Book(models.Model):
    """Book."""

    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    authors = models.ManyToManyField('books.Author', related_name='books')
    publisher = models.ForeignKey(Publisher,
                                  related_name='books',
                                  null=True,
                                  blank=True)
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

    class Meta(object):
        """Meta options."""

        ordering = ["isbn"]

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Order(models.Model):
    """Order."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    lines = models.ManyToManyField("books.OrderLine", blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta(object):
        """Meta options."""

        ordering = ["-created"]

    def __str__(self):
        return ugettext('Order')


@python_2_unicode_compatible
class OrderLine(models.Model):
    """Order line."""

    book = models.ForeignKey('books.Book', related_name='order_lines')

    class Meta(object):
        """Meta options."""

        ordering = ["order__created"]

    def __str__(self):
        return ugettext('{}').format(self.book.isbn)


@python_2_unicode_compatible
class Profile(models.Model):
    """Profile."""

    salutation = models.CharField(max_length=50)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    company_phone_number = models.CharField(max_length=200,
                                            null=True,
                                            blank=True)
    company_email = models.EmailField(null=True, blank=True)
    company_website = models.URLField(null=True, blank=True)

    bank_name = models.CharField(max_length=200, null=True, blank=True)
    bank_account_name = models.CharField(max_length=200, null=True, blank=True)
    bank_account_number = models.CharField(max_length=200,
                                           null=True,
                                           blank=True)

    # This does not cause a model change
    personal_information = NestedProxyField(
        'salutation',
        'first_name',
        'last_name',
        'birth_date',
        'biography'
    )

    # This does not cause a model change
    personal_contact_information = NestedProxyField(
        'email',
        'phone_number',
        'website',
    )

    # This does not cause a model change
    business_contact_information = NestedProxyField(
        'company',
        'company_email',
        'company_phone_number',
        'company_website',
    )

    # This does not cause a model change
    contact_information = NestedProxyField(
        'personal_contact_information',
        'business_contact_information',
    )

    # This does not cause a model change
    bank_information = NestedProxyField(
        'bank_name',
        'bank_account_name',
        'bank_account_number',
    )

    # This does not cause a model change
    data = NestedProxyField(
        'personal_information',
        'contact_information',
        'bank_information',
    )

    # This does not cause a model change
    information = NestedProxyField(
        'data',
    )

    # This is the structure we want to achieve
    # {
    #    'information': {
    #         'data': {
    #             'personal_information': (
    #                 'salutation',
    #                 'first_name',
    #                 'last_name',
    #                 'birth_date',
    #                 'biography',
    #             ),
    #             'contact_information': {
    #                 'personal_contact_information': (
    #                     'email',
    #                     'phone_number',
    #                     'website',
    #                 ),
    #                 'business_contact_information': (
    #                     'company',
    #                     'company_email',
    #                     'company_phone_number',
    #                     'company_website',
    #                 )
    #             },
    #             'bank_information': (
    #                 'bank_name',
    #                 'bank_account_name',
    #                 'bank_account_number',
    #             ),
    #         }
    #     }
    # }

    class Meta(object):
        """Meta options."""

        ordering = ["id"]

    def __str__(self):
        return self.name
