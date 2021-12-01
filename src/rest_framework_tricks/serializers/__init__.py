"""
Serializers.
"""

from .nested_proxy import *

__title__ = "rest_framework_tricks.serializers"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = (
    "extract_nested_serializers",
    "HyperlinkedModelSerializer",
    "is_nested_proxy_field",
    "ModelSerializer",
    "NestedProxyFieldIdentifier",
    "set_instance_values",
)
