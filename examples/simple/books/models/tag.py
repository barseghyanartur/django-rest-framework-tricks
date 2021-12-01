"""
Tag models.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = ("Tag",)


class Tag(models.Model):
    """Simple tag model."""

    title = models.CharField(max_length=255, unique=True)

    class Meta:
        """Meta options."""

        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.title
