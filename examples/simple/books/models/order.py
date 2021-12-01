"""
Order models.
"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext

__all__ = (
    'Order',
)


class Order(models.Model):
    """Order."""

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    lines = models.ManyToManyField("books.OrderLine", blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        """Meta options."""

        ordering = ["-created"]

    def __str__(self):
        return gettext('Order')
