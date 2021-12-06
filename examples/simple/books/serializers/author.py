"""
Author serializers.
"""

from rest_framework import serializers
from rest_framework_tricks.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
)

from ..models import (
    Author,
    AuthorProxy,
)

__all__ = (
    "AuthorProxySerializer",
    "AuthorSerializer",
)


# ****************************************************************************
# ******************************** Author ************************************
# ****************************************************************************


class PersonalContactInformationSerializer(serializers.ModelSerializer):
    """Personal contact information serializer."""

    class Meta:
        """Meta options."""

        model = Author
        fields = (
            "email",
            "phone_number",
            "website",
        )
        nested_proxy_field = True


class BusinessContactInformationSerializer(serializers.ModelSerializer):
    """Business contact information serializer."""

    class Meta:
        """Meta options."""

        model = Author
        fields = (
            "company",
            "company_email",
            "company_phone_number",
            "company_website",
        )
        nested_proxy_field = True


class ContactInformationSerializer(serializers.ModelSerializer):
    """Contact information serializer."""

    personal_contact_information = PersonalContactInformationSerializer(
        required=False
    )
    business_contact_information = BusinessContactInformationSerializer(
        required=False
    )

    class Meta:
        """Meta options."""

        model = Author
        fields = (
            "personal_contact_information",
            "business_contact_information",
        )
        nested_proxy_field = True


class AuthorSerializer(ModelSerializer):
    """Author serializer."""

    contact_information = ContactInformationSerializer(required=False)

    class Meta:
        """Meta options."""

        model = Author
        fields = (
            "id",
            "salutation",
            "name",
            "birth_date",
            "biography",
            "contact_information",
        )


# ****************************************************************************
# ****************************** AuthorProxy *********************************
# ****************************************************************************


class ProxyPersonalContactInformationSerializer(serializers.ModelSerializer):
    """Personal contact information serializer."""

    class Meta:
        """Meta options."""

        model = AuthorProxy
        fields = (
            "email",
            "phone_number",
            "website",
        )
        nested_proxy_field = True


class ProxyBusinessContactInformationSerializer(serializers.ModelSerializer):
    """Business contact information serializer."""

    class Meta:
        """Meta options."""

        model = AuthorProxy
        fields = (
            "company",
            "company_email",
            "company_phone_number",
            "company_website",
        )
        nested_proxy_field = True


class ProxyContactInformationSerializer(serializers.ModelSerializer):
    """Contact information serializer."""

    personal_contact_information = ProxyPersonalContactInformationSerializer(
        required=False
    )
    business_contact_information = ProxyBusinessContactInformationSerializer(
        required=False
    )

    class Meta:
        """Meta options."""

        model = AuthorProxy
        fields = (
            "personal_contact_information",
            "business_contact_information",
        )
        nested_proxy_field = True


class AuthorProxySerializer(ModelSerializer):
    """Author serializer."""

    contact_information = ProxyContactInformationSerializer(required=False)

    class Meta:
        """Meta options."""

        model = AuthorProxy
        fields = (
            "id",
            "salutation",
            "name",
            "birth_date",
            "biography",
            "contact_information",
        )
