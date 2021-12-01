"""
Profile serializers.
"""

from rest_framework import serializers
from rest_framework_tricks.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
)

from ..models import Profile

__all__ = ("ProfileSerializer",)

# ****************************************************************************
# ******************************* Profile ************************************
# ****************************************************************************


class PersonalInformationSerializer(serializers.ModelSerializer):
    """Personal information serializer."""

    class Meta:
        """Meta options."""

        model = Profile
        fields = (
            "salutation",
            "first_name",
            "last_name",
            "birth_date",
            "biography",
        )
        nested_proxy_field = True


class PersonalContactInformationSerializer(serializers.ModelSerializer):
    """Personal contact information serializer."""

    class Meta:
        """Meta options."""

        model = Profile
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

        model = Profile
        fields = (
            "company",
            "company_email",
            "company_phone_number",
            "company_website",
        )
        nested_proxy_field = True


class ContactInformationSerializer(serializers.ModelSerializer):
    """Contact information serializer."""

    personal_contact_information = PersonalContactInformationSerializer(required=False)
    business_contact_information = BusinessContactInformationSerializer(required=False)

    class Meta:
        """Meta options."""

        model = Profile
        fields = (
            "personal_contact_information",
            "business_contact_information",
        )
        nested_proxy_field = True


class BankInformationSerializer(serializers.ModelSerializer):
    """Bank information serializer."""

    class Meta:
        """Meta options."""

        model = Profile
        fields = (
            "bank_name",
            "bank_account_name",
            "bank_account_number",
        )
        nested_proxy_field = True


class DataSerializer(serializers.ModelSerializer):
    """Data serializer."""

    personal_information = PersonalInformationSerializer(required=False)
    contact_information = ContactInformationSerializer(required=False)
    bank_information = BankInformationSerializer(required=False)

    class Meta:
        """Meta options."""

        model = Profile
        fields = (
            "personal_information",
            "contact_information",
            "bank_information",
        )
        nested_proxy_field = True


class InformationSerializer(serializers.ModelSerializer):
    """information serializer."""

    data = DataSerializer(required=False)

    class Meta:
        """Meta options."""

        model = Profile
        fields = ("data",)
        nested_proxy_field = True


class ProfileSerializer(ModelSerializer):
    """Profile serializer."""

    information = InformationSerializer(required=False)

    class Meta:
        """Meta options."""

        model = Profile
        fields = (
            "id",
            "information",
        )
