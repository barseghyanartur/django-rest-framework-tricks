"""
Publisher models.
"""

from django.db import models
from rest_framework_tricks.models.fields import NestedProxyField

__all__ = (
    'Publisher',
)


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

    class Meta:
        """Meta options."""

        ordering = ["id"]

    def __str__(self):
        return self.name
