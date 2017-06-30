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
    >>>     class Meta(object):
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
    >>>     class Meta(object):
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


__title__ = 'rest_framework_tricks.serializers.nested_proxy'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'HyperlinkedModelSerializer',
    'is_nested_proxy_field',
    'ModelSerializer',
    'NestedProxyFieldIdentifier',
)


def is_nested_proxy_field(field):
    """Checks if field is nested proxy field."""
    return (
        isinstance(field, NestedProxyFieldIdentifier)
        or
        (
            getattr(field, 'Meta', False)
            and
            getattr(field.Meta, 'nested_proxy_field', False)
        )
    )


class NestedProxyFieldIdentifier(object):
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
    >>>     class Meta(object):
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
        __nested_serializers = {}
        for __field_name, __field in self.fields.items():
            if is_nested_proxy_field(__field):
                __nested_serializers[__field_name] = validated_data.pop(
                    __field_name
                )

        # Create instance, but don't save it yet
        instance = self.Meta.model(**validated_data)

        # Assign fields one by one
        for __serializer_name, __serializer in __nested_serializers.items():
            for __field_name, __field_value in __serializer.items():
                setattr(instance, __field_name, __field_value)

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
        __nested_serializers = {}
        for __field_name, __field in self.fields.items():
            if is_nested_proxy_field(__field):
                __nested_serializers[__field_name] = validated_data.pop(
                    __field_name
                )

        # Update the instance
        instance = super(ModelSerializer, self).update(
            instance,
            validated_data
        )

        # Assign fields one by one
        for __serializer_name, __serializer in __nested_serializers.items():

            for __field_name, __field_value in __serializer.items():
                setattr(instance, __field_name, __field_value)

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
    >>>     class Meta(object):
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
        __nested_serializers = {}
        for __field_name, __field in self.fields.items():
            if is_nested_proxy_field(__field) \
                    and __field_name in validated_data:
                __nested_serializers[__field_name] = validated_data.pop(
                    __field_name
                )

        # Create instance, but don't save it yet
        instance = self.Meta.model(**validated_data)

        # Assign fields one by one
        for __serializer_name, __serializer in __nested_serializers.items():
            for __field_name, __field_value in __serializer.items():
                setattr(instance, __field_name, __field_value)

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
        __nested_serializers = {}
        for __field_name, __field in self.fields.items():
            if is_nested_proxy_field(__field) \
                    and __field_name in validated_data:
                __nested_serializers[__field_name] = validated_data.pop(
                    __field_name
                )

        # Update the instance
        instance = super(HyperlinkedModelSerializer, self).update(
            instance,
            validated_data
        )

        # Assign fields one by one
        for __serializer_name, __serializer in __nested_serializers.items():
            for __field_name, __field_value in __serializer.items():
                setattr(instance, __field_name, __field_value)

        # Save the instance and return
        instance.save()
        return instance
