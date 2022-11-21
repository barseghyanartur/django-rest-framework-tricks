from copy import deepcopy

from django.utils.translation import gettext_lazy as _
from humanize import naturalsize
from rest_framework.fields import FileField

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2017-2022 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = ("ConstrainedFileField",)


class ConstrainedFileField(FileField):
    """A FileField with additional constraints.

    Namely, the file size can be restricted.

    Parameters:
        max_upload_size : int
            Maximum file size allowed for upload, in bytes
                1 MB - 1_048_576 B - 1024**2 B - 2**20 B
                2.5 MB - 2_621_440 B
                5 MB - 5_242_880 B
                10 MB - 10_485_760 B
                20 MB - 20_971_520 B
                33 MiB - 2**25 B
                50 MB - 5_242_880 B
                100 MB 104_857_600 B
                250 MB - 214_958_080 B
                500 MB - 429_916_160 B
                1 GiB - 1024 MiB - 2**30 B
    """

    default_error_messages = deepcopy(FileField.default_error_messages)
    default_error_messages.update(
        {
            "max_upload_size": _(
                "File size exceeds limit: {current_size}. "
                "Limit is {max_size}."
            )
        }
    )

    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop("max_upload_size", 0)
        assert (
            isinstance(self.max_upload_size, int) and self.max_upload_size >= 0
        )
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        if self.max_upload_size and data.size > self.max_upload_size:
            # Raise errors when needed
            self.fail(
                "max_upload_size",
                current_size=naturalsize(data.size, False, True),
                max_size=naturalsize(self.max_upload_size, False, True),
            )

        return data
