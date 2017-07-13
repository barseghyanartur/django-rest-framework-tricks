=======================
Advanced usage examples
=======================

Contents:

.. contents:: Table of Contents

Nested serializers
==================

Unlimited nesting depth
-----------------------

Our imaginary ``Author`` model consist of the following (non-relational)
Django model fields:

- ``salutation``: ``CharField``
- ``name``: ``CharField``
- ``email``: ``EmailField``
- ``birth_date``: ``DateField``
- ``biography``: ``TextField``
- ``phone_number``: ``CharField``
- ``website``: ``URLField``
- ``company``: ``CharField``
- ``company_phone_number``: ``CharField``
- ``company_email``: ``EmailField``
- ``company_website``: ``URLField``

In our REST API, we split the Author serializer into parts using nested
serializers to have the following structure:

.. code-block:: javascript

    {
        "id": "",
        "salutation": "",
        "name": "",
        "birth_date": "",
        "biography": "",
        "contact_information": {
            "personal_contact_information": {
                "email": "",
                "phone_number": "",
                "website": ""
            },
            "business_contact_information": {
                "company": "",
                "company_email": "",
                "company_phone_number": "",
                "company_website": ""
            }
        }
    }

Sample models
~~~~~~~~~~~~~

The only variation from standard implementation here is that we declare two
``NestedProxyField`` fields on the ``Author`` model level for to be used in
``AuthorSerializer`` serializer.

Note, that the change does not cause model change (no migrations or
whatsoever).

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

        # List the fields for `PersonalContactInformationSerializer` nested
        # serializer. This does not cause a model change.
        personal_contact_information = NestedProxyField(
            'email',
            'phone_number',
            'website',
        )

        # List the fields for `BusinessContactInformationSerializer` nested
        # serializer. This does not cause a model change.
        business_contact_information = NestedProxyField(
            'company',
            'company_email',
            'company_phone_number',
            'company_website',
        )

        # List the fields for `ContactInformationSerializer` nested
        # serializer. This does not cause a model change.
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
    # List the fields for `ContactInformationSerializer` nested
    # serializer. This does not cause a model change.
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

At first, we add ``nested_proxy_field`` property to the ``Meta`` class
definitions  of ``PersonalContactInformationSerializer``,
``BusinessContactInformationSerializer`` and ``ContactInformationSerializer``
nested serializers.

Then we define our (main) ``AuthorSerializer`` class, which is going to be
used a ``serializer_class`` of the ``AuthorViewSet``. We inherit the
``AuthorSerializer`` from
``rest_framework_tricks.serializers.HyperlinkedModelSerializer``
instead of the one of the Django REST framework. There's also a
``rest_framework_tricks.serializers.ModelSerializer`` available.

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

.. note::

    If you get validation errors about null-values, add ``allow_null=True``
    next to the ``required=False`` for serializer field definitions.

**Nested serializer for `ContactInformationSerializer` nested serializer**

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

**Nested serializer for `ContactInformationSerializer` nested serializer**

.. code-block:: python

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

**Nested serializer for `AuthorSerializer` (main) serializer**

.. code-block:: python

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

**Main serializer to be used in the ViewSet**

.. code-block:: python

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

If you can't make use of `rest_framework_tricks` serializers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If somehow you can't make use of the
``rest_framework_tricks.serializers.ModelSerializer`` or
``rest_framework_tricks.serializers.HyperlinkedModelSerializer`` serializers,
there are handy functions to help you to make your serializer to work with
``NestedProxyField``.

See the following example:

Required imports
++++++++++++++++

.. code-block:: python

    from rest_framework import serializers
    from rest_framework_tricks.serializers.nested_proxy import (
        extract_nested_serializers,
        set_instance_values,
    )

Serializer definition
+++++++++++++++++++++

.. code-block:: python

    class BookSerializer(serializers.ModelSerializer):
        """BookSerializer."""

        # ...

        def create(self, validated_data):
            """Create.

            :param validated_data:
            :return:
            """
            # Collect information on nested serializers
            __nested_serializers, __nested_serializers_data = \
                extract_nested_serializers(
                    self,
                    validated_data,
                )

            # Create instance, but don't save it yet
            instance = self.Meta.model(**validated_data)

            # Assign fields to the `instance` one by one
            set_instance_values(
                __nested_serializers,
                __nested_serializers_data,
                instance
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
            __nested_serializers, __nested_serializers_data = \
                extract_nested_serializers(
                    self,
                    validated_data,
                )

            # Update the instance
            instance = super(ModelSerializer, self).update(
                instance,
                validated_data
            )

            # Assign fields to the `instance` one by one
            set_instance_values(
                __nested_serializers,
                __nested_serializers_data,
                instance
            )

            # Save the instance and return
            instance.save()
            return instance

Sample ViewSet
~~~~~~~~~~~~~~

Absolutely no variations from standard implementation here.

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

Absolutely no variations from standard implementation here.

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
                "company_phone_number": "+386-35-5689443",
                "company_website": "http://www.xifyhefiqom.com.au"
            }
        }
    }
