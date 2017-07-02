from .nested_proxy import *

__title__ = 'rest_framework_tricks.serializers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'extract_nested_serializers',
    'HyperlinkedModelSerializer',
    'is_nested_proxy_field',
    'ModelSerializer',
    'NestedProxyFieldIdentifier',
    'set_instance_values',
)
