"""
Profile serializers.
"""

from rest_framework import serializers
from rest_framework_tricks.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
)

from ..models import Payment

__all__ = (
    'PaymentSerializer',
)

# ****************************************************************************
# ******************************* Profile ************************************
# ****************************************************************************


class BuyerSerializer(serializers.ModelSerializer):
    """Buyer serializer."""

    class Meta:
        """Meta options."""

        model = Payment
        fields = (
            'buyer_salutation',
            'buyer_name',
            'buyer_email',
            'buyer_headshot',
            'buyer_birth_date',
            "buyer_biography",
            "buyer_phone_number",
            "buyer_website",
        )
        nested_proxy_field = True


class CompanySerializer(serializers.ModelSerializer):
    """Company serializer."""

    class Meta:
        """Meta options."""

        model = Payment
        fields = (
            'company_name',
            'company_phone_number',
            'company_email',
            "company_website",
        )
        nested_proxy_field = True

#
# class BusinessContactInformationSerializer(serializers.ModelSerializer):
#     """Business contact information serializer."""
#
#     class Meta:
#         """Meta options."""
#
#         model = Payment
#         fields = (
#             'company_name',
#             'company_email',
#             'company_phone_number',
#             'company_website',
#         )
#         nested_proxy_field = True
#
#
# class ContactInformationSerializer(serializers.ModelSerializer):
#     """Contact information serializer."""
#
#     personal_contact_information = PersonalContactInformationSerializer(
#         required=False
#     )
#     business_contact_information = BusinessContactInformationSerializer(
#         required=False
#     )
#
#     class Meta(object):
#         """Meta options."""
#
#         model = Profile
#         fields = (
#             'personal_contact_information',
#             'business_contact_information',
#         )
#         nested_proxy_field = True
#
#
# class BankInformationSerializer(serializers.ModelSerializer):
#     """Bank information serializer."""
#
#     class Meta(object):
#         """Meta options."""
#
#         model = Profile
#         fields = (
#             'bank_name',
#             'bank_account_name',
#             'bank_account_number',
#         )
#         nested_proxy_field = True
#
#
# class DataSerializer(serializers.ModelSerializer):
#     """Data serializer."""
#
#     personal_information = PersonalInformationSerializer(
#         required=False
#     )
#     contact_information = ContactInformationSerializer(
#         required=False
#     )
#     bank_information = BankInformationSerializer(
#         required=False
#     )
#
#     class Meta(object):
#         """Meta options."""
#
#         model = Profile
#         fields = (
#             'personal_information',
#             'contact_information',
#             'bank_information',
#         )
#         nested_proxy_field = True
#
#
# class InformationSerializer(serializers.ModelSerializer):
#     """information serializer."""
#
#     data = DataSerializer(
#         required=False
#     )
#
#     class Meta(object):
#         """Meta options."""
#
#         model = Profile
#         fields = (
#             'data',
#         )
#         nested_proxy_field = True


class PaymentSerializer(ModelSerializer):
    """Payment serializer."""

    buyer = BuyerSerializer(required=False)
    company = CompanySerializer(required=False)

    class Meta(object):
        """Meta options."""

        model = Payment
        fields = (
            'id',
            'information',
        )
