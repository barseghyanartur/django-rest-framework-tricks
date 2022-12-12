from copy import deepcopy
from typing import List, Dict, Any

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2017-2022 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = (
    "get_nested_data_field_names",
    "flatten_nested_data",
)


def get_nested_data_field_names(serializer) -> List[str]:
    """Get nested data field names."""
    nested_field_names = []
    for field_name, field in serializer.fields.items():
        if getattr(field, "Meta", None) and getattr(
            field.Meta, "nested_proxy_field", False
        ):
            nested_field_names.append(field_name)
    return nested_field_names


def flatten_nested_data(
    validated_data: Dict[str, Any], nested_field_names: List[str]
) -> Dict[str, Any]:
    """Flatten nested data.

    Usage example:

        class MySerializer(serializers.ModelSerializer):

            def create(self, validated_data):
                # Do something else
                nested_field_names = get_nested_field_names(self)
                validated_data = flatten_nested_data(
                    validated_data, nested_field_names
                )
                return super().create(validated_data)
    """
    validated_data = deepcopy(validated_data)
    for field_name in nested_field_names:
        data = validated_data.pop(field_name, None)
        if data:
            validated_data.update(data)
    return validated_data
