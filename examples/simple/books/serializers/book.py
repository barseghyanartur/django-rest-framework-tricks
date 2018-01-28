"""
Book serializers.
"""

from rest_framework import serializers
from rest_framework_tricks.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
)

from ..models import Book, BookProxy, BookProxy2

__all__ = (
    'BookSerializer',
    'BookProxySerializer',
    'BookProxy2Serializer',
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
    city = serializers.CharField(source='publisher.city', read_only=True)

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
            'city',
        )

# ****************************************************************************
# ***************************** BookProxy ************************************
# ****************************************************************************


class BookProxy2Serializer(HyperlinkedModelSerializer):
    """Book proxy serializer."""

    publishing_information = PublishingInformationSerializer(required=False)
    stock_information = StockInformationSerializer(required=False)
    city = serializers.CharField(source='publisher.city', read_only=True)

    class Meta(object):
        """Meta options."""

        model = BookProxy2
        fields = (
            'url',
            'id',
            'title',
            'description',
            'summary',
            'publishing_information',
            'stock_information',
            'city',
        )
