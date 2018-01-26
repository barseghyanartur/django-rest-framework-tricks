"""
Order line models.
"""

from django.db import models
from django.utils.translation import ugettext

from six import python_2_unicode_compatible

__all__ = (
    'OrderLine',
)


@python_2_unicode_compatible
class OrderLine(models.Model):
    """Order line."""

    book = models.ForeignKey(
        'books.Book',
        related_name='order_lines',
        on_delete=models.CASCADE
    )

    class Meta(object):
        """Meta options."""

        ordering = ["order__created"]

    def __str__(self):
        return ugettext('{}').format(self.book.isbn)
