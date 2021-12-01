"""
Author model.
"""

from django.db import models

from rest_framework_tricks.models.fields import NestedProxyField

__all__ = (
    'Payment',
    "PaymentProxy",
)


class Payment(models.Model):
    """Payment."""

    buyer_salutation = models.CharField(max_length=10)
    buyer_name = models.CharField(max_length=200)
    buyer_email = models.EmailField()
    buyer_headshot = models.ImageField(upload_to='authors', null=True, blank=True)
    buyer_birth_date = models.DateField(null=True, blank=True)
    buyer_biography = models.TextField(null=True, blank=True)
    buyer_phone_number = models.CharField(max_length=200, null=True, blank=True)
    buyer_website = models.URLField(null=True, blank=True)

    company_name = models.CharField(max_length=200, null=True, blank=True)
    company_phone_number = models.CharField(max_length=200,
                                            null=True,
                                            blank=True)
    company_email = models.EmailField(null=True, blank=True)
    company_website = models.URLField(null=True, blank=True)

    # This does not cause a model change
    contact_information = NestedProxyField(
        {
            'buyer': (
                ('email', "buyer_email"),
                ('phone_number', "buyer_phone_number"),
                ('website', "buyer_website"),
            )
        },
        {
            'company': (
                ("name", "company_name"),
                ("email", 'company_email',),
                ("phone_number", 'company_phone_number',),
                ("website", 'company_website',),
            )
        },
    )

    class Meta:
        """Meta options."""

        ordering = ["id"]

    def __str__(self):
        return self.name


class PaymentProxy(Payment):
    """Payment proxy model for to be used in testing."""

    # This does not cause a model change
    buyer = NestedProxyField(
        'email',
        'phone_number',
        'website',
    )

    # This does not cause a model change
    company = NestedProxyField(
        ("name", "company_name"),
        ("email", 'company_email',),
        ("phone_number", 'company_phone_number',),
        ("website", 'company_website',),
    )

    # This does not cause a model change
    contact_information = NestedProxyField(
        'buyer',
        'company',
    )

    class Meta:
        """Meta options."""

        proxy = True
