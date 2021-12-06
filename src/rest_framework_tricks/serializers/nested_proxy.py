"""
Serializers.

The following code is used in the usage examples of the ``ModelSerializer``
and ``HyperlinkedModelSerializer`` classes.

    >>> from rest_framework import serializers
    >>>
    >>> from .models import Book
    >>>
    >>>
    >>> class PublishingInformationSerializer(serializers.ModelSerializer):
    >>>
    >>>     publication_date = serializers.DateField(required=False)
    >>>     isbn = serializers.CharField(required=False)
    >>>     pages = serializers.IntegerField(required=False)
    >>>
    >>>     class Meta:
    >>>
    >>>         model = Book
    >>>         fields = (
    >>>             'publication_date',
    >>>             'isbn',
    >>>             'pages',
    >>>         )
    >>>         nested_proxy_field = True
    >>>
    >>>
    >>> class StockInformationSerializer(serializers.ModelSerializer):
    >>>
    >>>     class Meta:
    >>>
    >>>         model = Book
    >>>         fields = (
    >>>             'stock_count',
    >>>             'price',
    >>>             'state',
    >>>         )
    >>>         nested_proxy_field = True
"""

from rest_framework import serializers


__title__ = "rest_framework_tricks.serializers.nested_proxy"
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


def is_nested_proxy_field(field):
    """Check if field is nested proxy field.

    :param field:
    :type field:
    :return: True or False
    :rtype: bool
    """
    return isinstance(field, NestedProxyFieldIdentifier) or (
        getattr(field, "Meta", False)
        and getattr(field.Meta, "nested_proxy_field", False)
    )


def extract_nested_serializers(
    serializer,
    validated_data,
    nested_serializers=None,
    nested_serializers_data=None,
):
    """Extract nested serializers.

    :param serializer: Serializer instance.
    :param validated_data: Validated data.
    :param nested_serializers:
    :param nested_serializers_data:
    :type serializer: rest_framework.serializers.Serializer
    :type validated_data: dict
    :type nested_serializers: dict
    :type nested_serializers_data:
    :return:
    :rtype: tuple
    """
    if nested_serializers is None:
        nested_serializers = {}
    if nested_serializers_data is None:
        nested_serializers_data = {}

    for __field_name, __field in serializer.fields.items():
        if is_nested_proxy_field(__field) and __field_name in validated_data:
            __serializer_data = validated_data.pop(__field_name)
            nested_serializers[__field_name] = __field
            nested_serializers_data[__field_name] = __serializer_data

    return nested_serializers, nested_serializers_data


def set_instance_values(nested_serializers, nested_serializers_data, instance):
    """Set values on instance.

    Does not perform any save actions.

    :param nested_serializers: Nested serializers.
    :param nested_serializers_data: Nested serializers data.
    :param instance: Instance (not yet saved)
    :type nested_serializers:
    :type nested_serializers_data:
    :type instance:
    :return: Same instance with values set.
    :rtype:
    """
    for __serializer_name, __serializer in nested_serializers_data.items():
        for __field_name, __field_value in __serializer.items():
            if is_nested_proxy_field(
                nested_serializers[__serializer_name][__field_name]
            ):
                set_instance_values(
                    {
                        __field_name: nested_serializers[__serializer_name][
                            __field_name
                        ]
                    },
                    {__field_name: __field_value},
                    instance,
                )
            else:
                setattr(instance, __field_name, __field_value)


class NestedProxyFieldIdentifier:
    """NestedProxyField identifier."""


class ModelSerializer(serializers.ModelSerializer):
    """ModelSerializer for models with NestedProxyField fields.

    Example:

    >>> from rest_framework_tricks.serializers import ModelSerializer
    >>>
    >>>
    >>> class BookSerializer(ModelSerializer):
    >>>
    >>>     publishing_information = PublishingInformationSerializer(
    >>>         required=False
    >>>     )
    >>>     stock_information = StockInformationSerializer(required=False)
    >>>
    >>>     class Meta:
    >>>
    >>>         model = Book
    >>>         fields = (
    >>>             'url',
    >>>             'id',
    >>>             'title',
    >>>             'description',
    >>>             'summary',
    >>>             'publishing_information',
    >>>             'stock_information',
    >>>         )
    """

    def create(self, validated_data):
        """Create.

        :param validated_data:
        :return:
        """
        # Collect information on nested serializers
        (
            __nested_serializers,
            __nested_serializers_data,
        ) = extract_nested_serializers(
            self,
            validated_data,
        )

        # Create instance, but don't save it yet
        instance = self.Meta.model(**validated_data)

        # Assign fields to the `instance` one by one
        set_instance_values(
            __nested_serializers, __nested_serializers_data, instance
        )

        # Save the instance and return
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """Update.

        :param instance:
        :param validated_data:
        :return:
        """
        # Collect information on nested serializers
        (
            __nested_serializers,
            __nested_serializers_data,
        ) = extract_nested_serializers(
            self,
            validated_data,
        )

        # Update the instance
        instance = super(ModelSerializer, self).update(
            instance, validated_data
        )

        # Assign fields to the `instance` one by one
        set_instance_values(
            __nested_serializers, __nested_serializers_data, instance
        )

        # Save the instance and return
        instance.save()
        return instance


class HyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    """HyperlinkedModelSerializer for models with NestedProxyField fields.

    Example:

    >>> from rest_framework_tricks.serializers import (
    >>>     HyperlinkedModelSerializer,
    >>> )
    >>>
    >>>
    >>> class BookSerializer(HyperlinkedModelSerializer):
    >>>
    >>>     publishing_information = PublishingInformationSerializer(
    >>>         required=False
    >>>     )
    >>>     stock_information = StockInformationSerializer(required=False)
    >>>
    >>>     class Meta:
    >>>
    >>>         model = Book
    >>>         fields = (
    >>>             'url',
    >>>             'id',
    >>>             'title',
    >>>             'description',
    >>>             'summary',
    >>>             'publishing_information',
    >>>             'stock_information',
    >>>         )
    """

    def create(self, validated_data):
        """Create.

        :param validated_data:
        :return:
        """
        # Collect information on nested serializers
        (
            __nested_serializers,
            __nested_serializers_data,
        ) = extract_nested_serializers(
            self,
            validated_data,
        )

        # Create instance, but don't save it yet
        instance = self.Meta.model(**validated_data)

        # Assign fields to the `instance` one by one
        set_instance_values(
            __nested_serializers, __nested_serializers_data, instance
        )

        # Save the instance and return
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """Update.

        :param instance:
        :param validated_data:
        :return:
        """
        # Collect information on nested serializers
        (
            __nested_serializers,
            __nested_serializers_data,
        ) = extract_nested_serializers(
            self,
            validated_data,
        )

        # Update the instance
        instance = super(HyperlinkedModelSerializer, self).update(
            instance, validated_data
        )

        # Assign fields to the `instance` one by one
        set_instance_values(
            __nested_serializers, __nested_serializers_data, instance
        )

        # Save the instance and return
        instance.save()
        return instance
