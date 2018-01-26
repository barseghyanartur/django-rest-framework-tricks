"""
Book serializers.
"""

from rest_framework import serializers
from rest_framework_tricks.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
)

from ..models import Book, BookProxy

__all__ = (
    'BookSerializer',
    'BookProxySerializer',
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
# ***************************** BookProxy ************************************
# ****************************************************************************


class BookProxySerializer(HyperlinkedModelSerializer):
    """Book proxy serializer."""

    publishing_information = PublishingInformationSerializer(required=False)
    stock_information = StockInformationSerializer(required=False)
    publisher_name = serializers.CharField(source='publisher.name')

    class Meta(object):
        """Meta options."""

        model = BookProxy
        fields = (
            'url',
            'id',
            'title',
            'description',
            'summary',
            'publishing_information',
            'stock_information',
            'publisher_name',
        )
