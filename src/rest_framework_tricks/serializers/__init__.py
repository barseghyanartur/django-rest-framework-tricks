"""
Serializers.
"""

from .nested_proxy import *

__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2021 Artur Barseghyan'
__license__ = 'GPL-2.0-only OR LGPL-2.1-or-later'
__all__ = (
    'extract_nested_serializers',
    'HyperlinkedModelSerializer',
    'is_nested_proxy_field',
    'ModelSerializer',
    'NestedProxyFieldIdentifier',
    'set_instance_values',
)
