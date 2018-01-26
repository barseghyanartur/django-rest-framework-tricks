"""
Publisher serializers.
"""

from rest_framework import serializers
from rest_framework_tricks.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
)

from ..models import Publisher

__all__ = (
    'PublisherSerializer',
)

# ****************************************************************************
# ****************************** Publisher ***********************************
# ****************************************************************************


class AddressInformationSerializer(serializers.ModelSerializer):
    """Address information serializer."""

    address = serializers.CharField(required=False, allow_null=True)
    city = serializers.CharField(required=False, allow_null=True)
    state_province = serializers.CharField(required=False, allow_null=True)
    country = serializers.CharField(required=False, allow_null=True)

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
