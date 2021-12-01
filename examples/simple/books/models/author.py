"""
Author model.
"""

from django.db import models

from rest_framework_tricks.models.fields import NestedProxyField

__all__ = (
    'Author',
    'AuthorProxy',
)


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

    class Meta:
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

    class Meta:
        """Meta options."""

        proxy = True
