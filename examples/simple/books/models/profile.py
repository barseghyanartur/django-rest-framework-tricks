"""
Profile models.
"""

from django.db import models

from rest_framework_tricks.models.fields import NestedProxyField

__all__ = ("Profile",)


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
    company_phone_number = models.CharField(
        max_length=200, null=True, blank=True
    )
    company_email = models.EmailField(null=True, blank=True)
    company_website = models.URLField(null=True, blank=True)

    bank_name = models.CharField(max_length=200, null=True, blank=True)
    bank_account_name = models.CharField(max_length=200, null=True, blank=True)
    bank_account_number = models.CharField(
        max_length=200, null=True, blank=True
    )

    # This does not cause a model change
    personal_information = NestedProxyField(
        "salutation", "first_name", "last_name", "birth_date", "biography"
    )

    # This does not cause a model change
    personal_contact_information = NestedProxyField(
        "email",
        "phone_number",
        "website",
    )

    # This does not cause a model change
    business_contact_information = NestedProxyField(
        "company",
        "company_email",
        "company_phone_number",
        "company_website",
    )

    # This does not cause a model change
    contact_information = NestedProxyField(
        "personal_contact_information",
        "business_contact_information",
    )

    # This does not cause a model change
    bank_information = NestedProxyField(
        "bank_name",
        "bank_account_name",
        "bank_account_number",
    )

    # This does not cause a model change
    data = NestedProxyField(
        "personal_information",
        "contact_information",
        "bank_information",
    )

    # This does not cause a model change
    information = NestedProxyField(
        "data",
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

    class Meta:
        """Meta options."""

        ordering = ["id"]

    def __str__(self):
        return self.name
