"""
Test utils.
"""
import pytest

from ..utils import DictProxy

from .base import BaseTestCase

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2017-2022 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = ("TestUtils",)


@pytest.mark.django_db
class TestUtils(BaseTestCase):
    """Test utils."""

    pytestmark = pytest.mark.django_db

    def test_dict_proxy(self):
        """Test DictProxy."""

        __dict = {
            "name": self.faker.name(),
            "date": self.faker.date(),
        }

        __dict_proxy = DictProxy(__dict)

        for __key in __dict.keys():
            self.assertEqual(getattr(__dict_proxy, __key), __dict[__key])

        print(__dict_proxy)
