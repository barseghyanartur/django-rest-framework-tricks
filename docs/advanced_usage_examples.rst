=======================
Advanced usage examples
=======================

Nested serializers
==================

Unlimited nesting depth
-----------------------

Sample models
~~~~~~~~~~~~~

Required imports
^^^^^^^^^^^^^^^^

.. code-block:: python

    from django.db import models

    from rest_framework_tricks.models.fields import NestedProxyField

Model definition
^^^^^^^^^^^^^^^^

.. code-block:: python

    class Author(models.Model):
        """Author."""

        salutation = models.CharField(max_length=10)
        name = models.CharField(max_length=200)
        email = models.EmailField()
        birth_date = models.DateField(null=True, blank=True)
        biography = models.TextField(null=True, blank=True)
        phone_number = models.CharField(max_length=200, null=True, blank=True)
        website = models.URLField(null=True, blank=True)
        company = models.CharField(max_length=200, null=True, blank=True)
        company_phone_number = models.CharField(max_length=200,
                                                null=True,
                                                blank=True)
        company_email = models.EmailField(null=True, blank=True)
        company_website = models.URLField(null=True, blank=True)

        # This does not cause a model change
        personal_contact_information = NestedProxyField(
            'email',
            'phone_number',
            'website',
        )

        # This does not cause a model change
        business_contact_information = NestedProxyField(
            'company',
            'company_email',
            'company_phone_number',
            'company_website',
        )

        # This does not cause a model change
        contact_information = NestedProxyField(
            'personal_contact_information',
            'business_contact_information',
        )

        class Meta(object):
            """Meta options."""

            ordering = ["id"]

        def __str__(self):
            return self.name

Alternatively, you could rewrite the ``contact_information`` definition
as follows (although at the moment it's not the recommended approach):

.. code-block:: python

    # ...
    # This does not cause a model change
    contact_information = NestedProxyField(
        {
            'personal_contact_information': (
                'email',
                'phone_number',
                'website',
            )
        },
        {
            'business_contact_information': (
                'company',
                'company_email',
                'company_phone_number',
                'company_website',
            )
        },
    )
    # ...


Sample serializers
~~~~~~~~~~~~~~~~~~

Required imports
^^^^^^^^^^^^^^^^

.. code-block:: python

    from rest_framework import serializers
    from rest_framework_tricks.serializers import (
        HyperlinkedModelSerializer,
        ModelSerializer,
    )

Serializer definition
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    class PersonalContactInformationSerializer(serializers.ModelSerializer):
        """Personal contact information serializer."""

        class Meta(object):
            """Meta options."""

            model = Author
            fields = (
                'email',
                'phone_number',
                'website',
            )
            nested_proxy_field = True


    class BusinessContactInformationSerializer(serializers.ModelSerializer):
        """Business contact information serializer."""

        class Meta(object):
            """Meta options."""

            model = Author
            fields = (
                'company',
                'company_email',
                'company_phone_number',
                'company_website',
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

        class Meta(object):
            """Meta options."""

            model = Author
            fields = (
                'personal_contact_information',
                'business_contact_information',
            )
            nested_proxy_field = True


    class AuthorSerializer(ModelSerializer):
        """Author serializer."""

        contact_information = ContactInformationSerializer(required=False)

        class Meta(object):
            """Meta options."""

            model = Author
            fields = (
                'id',
                'salutation',
                'name',
                'birth_date',
                'biography',
                'contact_information',
            )

Sample ViewSet
~~~~~~~~~~~~~~

Required imports
^^^^^^^^^^^^^^^^

.. code-block:: python

    from rest_framework.viewsets import ModelViewSet
    from rest_framework.permissions import AllowAny

    from .models import Author
    from .serializers import AuthorSerializer

ViewSet definition
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    class AuthorViewSet(ModelViewSet):
        """Author ViewSet."""

        queryset = Author.objects.all()
        serializer_class = AuthorSerializer
        permission_classes = [AllowAny]

Sample URLs/router definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Required imports
^^^^^^^^^^^^^^^^

.. code-block:: python

    from django.conf.urls import url, include

    from rest_framework_extensions.routers import ExtendedDefaultRouter

    from .viewsets import AuthorViewSet

ViewSet definition
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    router = ExtendedDefaultRouter()
    authors = router.register(r'authors',
                              AuthorViewSet,
                              base_name='author')

    urlpatterns = [
        url(r'^api/', include(router.urls)),
    ]

Sample OPTIONS call
~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    OPTIONS /books/api/authors/
    HTTP 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

.. code-block:: javascript

    {
        "name": "Author List",
        "description": "Author ViewSet.",
        "renders": [
            "application/json",
            "text/html"
        ],
        "parses": [
            "application/json",
            "application/x-www-form-urlencoded",
            "multipart/form-data"
        ],
        "actions": {
            "POST": {
                "id": {
                    "type": "integer",
                    "required": false,
                    "read_only": true,
                    "label": "ID"
                },
                "salutation": {
                    "type": "string",
                    "required": true,
                    "read_only": false,
                    "label": "Salutation",
                    "max_length": 10
                },
                "name": {
                    "type": "string",
                    "required": true,
                    "read_only": false,
                    "label": "Name",
                    "max_length": 200
                },
                "birth_date": {
                    "type": "date",
                    "required": false,
                    "read_only": false,
                    "label": "Birth date"
                },
                "biography": {
                    "type": "string",
                    "required": false,
                    "read_only": false,
                    "label": "Biography"
                },
                "contact_information": {
                    "type": "nested object",
                    "required": false,
                    "read_only": false,
                    "label": "Contact information",
                    "children": {
                        "personal_contact_information": {
                            "type": "nested object",
                            "required": false,
                            "read_only": false,
                            "label": "Personal contact information",
                            "children": {
                                "email": {
                                    "type": "email",
                                    "required": true,
                                    "read_only": false,
                                    "label": "Email",
                                    "max_length": 254
                                },
                                "phone_number": {
                                    "type": "string",
                                    "required": false,
                                    "read_only": false,
                                    "label": "Phone number",
                                    "max_length": 200
                                },
                                "website": {
                                    "type": "url",
                                    "required": false,
                                    "read_only": false,
                                    "label": "Website",
                                    "max_length": 200
                                }
                            }
                        },
                        "business_contact_information": {
                            "type": "nested object",
                            "required": false,
                            "read_only": false,
                            "label": "Business contact information",
                            "children": {
                                "company": {
                                    "type": "string",
                                    "required": false,
                                    "read_only": false,
                                    "label": "Company",
                                    "max_length": 200
                                },
                                "company_email": {
                                    "type": "email",
                                    "required": false,
                                    "read_only": false,
                                    "label": "Company email",
                                    "max_length": 254
                                },
                                "company_phone_number": {
                                    "type": "string",
                                    "required": false,
                                    "read_only": false,
                                    "label": "Company phone number",
                                    "max_length": 200
                                },
                                "company_website": {
                                    "type": "url",
                                    "required": false,
                                    "read_only": false,
                                    "label": "Company website",
                                    "max_length": 200
                                }
                            }
                        }
                    }
                }
            }
        }
    }

Sample POST call
~~~~~~~~~~~~~~~~

.. code-block:: text

    POST /books/api/authors/
    HTTP 201 Created
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

.. code-block:: javascript

    {
        "id": 1000012,
        "salutation": "At eve",
        "name": "Shana Rodriquez",
        "birth_date": "2016-04-05",
        "biography": "Commodi facere voluptate ipsum veniam maxime obcaecati",
        "contact_information": {
            "personal_contact_information": {
                "email": "somasesu@yahoo.com",
                "phone_number": "+386-36-3715907",
                "website": "http://www.xazyvufugasi.biz"
            },
            "business_contact_information": {
                "company": "Hopkins and Mccoy Co",
                "company_email": "vevuciqa@yahoo.com",
                "company_phone_number": "Estrada Savage Inc",
                "company_website": "http://www.xifyhefiqom.com.au"
            }
        }
    }
