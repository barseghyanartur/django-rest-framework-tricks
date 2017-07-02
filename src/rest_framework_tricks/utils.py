"""
Utils.
"""

import json
from six import python_2_unicode_compatible

__title__ = 'rest_framework_tricks.utils'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'DictProxy',
)


@python_2_unicode_compatible
class DictProxy(object):
    """Dictionary proxy.

    Example:

    >>> from rest_framework_tricks.utils import DictProxy
    >>>
    >>>
    >>> __dict = {
    >>>     'name': self.faker.name(),
    >>>     'date': self.faker.date(),
    >>> }
    >>>
    >>> __dict_proxy = DictProxy(__dict)
    """

    def __init__(self, mapping):
        self.__mapping = mapping

    def __getattr__(self, item):
        return self.__mapping.get(item, None)

    def __str__(self):
        return json.dumps(self.__mapping)

    __repr__ = __str__
