from rest_framework import serializers
from rest_framework_tricks.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
)

from .models import Book, Publisher

__all__ = (
    'AddressInformationSerializer',
    'BookSerializer',
    'PublisherSerializer',
    'PublisherSerializer',
    'PublishingInformationSerializer',
    'StockInformationSerializer',
)

# ****************************************************************************
# ******************************** Book **************************************
# ****************************************************************************


class PublishingInformationSerializer(serializers.ModelSerializer):
    """Publishing information serializer."""

    publication_date = serializers.DateField(required=False)
    isbn = serializers.CharField(required=False)
    pages = serializers.IntegerField(required=False)

    class Meta(object):
        """Meta options."""

        model = Book
        fields = (
            'publication_date',
            'isbn',
            'pages',
        )
        nested_proxy_field = True


class StockInformationSerializer(serializers.ModelSerializer):
    """Stock information serializer."""

    class Meta(object):
        """Meta options."""

        model = Book
        fields = (
            'stock_count',
            'price',
            'state',
        )
        nested_proxy_field = True


class BookSerializer(HyperlinkedModelSerializer):
    """Book serializer."""

    publishing_information = PublishingInformationSerializer(required=False)
    stock_information = StockInformationSerializer(required=False)

    class Meta(object):
        """Meta options."""

        model = Book
        fields = (
            'url',
            'id',
            'title',
            'description',
            'summary',
            'publishing_information',
            'stock_information',
        )

# ****************************************************************************
# ****************************** Publisher ***********************************
# ****************************************************************************


class AddressInformationSerializer(serializers.ModelSerializer):
    """Address information serializer."""

    class Meta(object):
        """Meta options."""

        model = Publisher
        fields = (
            'address',
            'city',
            'state_province',
            'country',
        )
        nested_proxy_field = True


class PublisherSerializer(ModelSerializer):
    """Publisher serializer."""

    address_information = AddressInformationSerializer(required=False)

    class Meta(object):
        """Meta options."""

        model = Publisher
        fields = (
            'id',
            'name',
            'info',
            'website',
            'address_information',
        )
