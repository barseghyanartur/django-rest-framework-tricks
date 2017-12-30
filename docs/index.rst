============================
django-rest-framework-tricks
============================
Collection of various tricks for
`Django REST framework <https://pypi.python.org/pypi/djangorestframework>`_.

Prerequisites
=============

- Django 1.8, 1.9, 1.10, 1.11 and 2.0.
- Python 2.7, 3.4, 3.5, 3.6

Dependencies
============

- djangorestframework: Written with 3.6.3, tested with >=3.5.0,<=3.7.7. May
  work on earlier versions, although not guaranteed.

Installation
============

(1) Install latest stable version from PyPI:

    .. code-block:: sh

        pip install django-rest-framework-tricks

    or latest stable version from GitHub:

    .. code-block:: sh

        pip install https://github.com/barseghyanartur/django-rest-framework-tricks/archive/stable.tar.gz

    or latest stable version from BitBucket:

    .. code-block:: sh

        pip install https://bitbucket.org/barseghyanartur/django-rest-framework-tricks/get/stable.tar.gz

(2) Add ``rest_framework`` and ``rest_framework_tricks`` to ``INSTALLED_APPS``:

    .. code-block:: python

        INSTALLED_APPS = (
            # ...
            # REST framework
            'rest_framework',

            # REST framework tricks (this package)
            'rest_framework_tricks',

            # ...
        )

Documentation
=============

Documentation is available on `Read the Docs
<http://django-rest-framework-tricks.readthedocs.io/>`_.

Main features and highlights
============================

- `Nested serializers`_: Nested serializers for non-relational fields.

Usage examples
==============

Nested serializers
------------------

Nested serializers for non-relational fields.

Our imaginary ``Book`` model consists of the following (non-relational) Django
model fields:

- ``title``: ``CharField``
- ``description``: ``TextField``
- ``summary``: ``TextField``
- ``publication_date``: ``DateTimeField``
- ``state``: ``CharField`` (with choices)
- ``isbn``: ``CharField``
- ``price``: ``DecimalField``
- ``pages``: ``IntegerField``
- ``stock_count``: ``IntegerField``

In our REST API, we want to split the Book serializer into parts using nested
serializers to have the following structure:

.. code-block:: javascript

    {
        "id": "",
        "title": "",
        "description": "",
        "summary": "",
        "publishing_information": {
            "publication_date": "",
            "isbn": "",
            "pages": ""
        },
        "stock_information": {
            "stock_count": "",
            "price": "",
            "state": ""
        }
    }

Sample model
~~~~~~~~~~~~

The only variation from standard implementation here is that we declare two
``NestedProxyField`` fields on the ``Book`` model level for to be used in
``BookSerializer`` serializer.

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

    BOOK_PUBLISHING_STATUS_PUBLISHED = 'published'
    BOOK_PUBLISHING_STATUS_NOT_PUBLISHED = 'not_published'
    BOOK_PUBLISHING_STATUS_IN_PROGRESS = 'in_progress'
    BOOK_PUBLISHING_STATUS_CHOICES = (
        (BOOK_PUBLISHING_STATUS_PUBLISHED, "Published"),
        (BOOK_PUBLISHING_STATUS_NOT_PUBLISHED, "Not published"),
        (BOOK_PUBLISHING_STATUS_IN_PROGRESS, "In progress"),
    )
    BOOK_PUBLISHING_STATUS_DEFAULT = BOOK_PUBLISHING_STATUS_PUBLISHED


    class Book(models.Model):
        """Book."""

        title = models.CharField(max_length=100)
        description = models.TextField(null=True, blank=True)
        summary = models.TextField(null=True, blank=True)
        publication_date = models.DateField()
        state = models.CharField(max_length=100,
                                 choices=BOOK_PUBLISHING_STATUS_CHOICES,
                                 default=BOOK_PUBLISHING_STATUS_DEFAULT)
        isbn = models.CharField(max_length=100, unique=True)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        pages = models.PositiveIntegerField(default=200)
        stock_count = models.PositiveIntegerField(default=30)

        # List the fields for `PublishingInformationSerializer` nested
        # serializer. This does not cause a model change.
        publishing_information = NestedProxyField(
            'publication_date',
            'isbn',
            'pages',
        )

        # List the fields for `StockInformationSerializer` nested serializer.
        # This does not cause a model change.
        stock_information = NestedProxyField(
            'stock_count',
            'price',
            'state',
        )

        class Meta(object):
            """Meta options."""

            ordering = ["isbn"]

        def __str__(self):
            return self.title

Sample serializers
~~~~~~~~~~~~~~~~~~

At first, we add ``nested_proxy_field`` property to the ``Meta`` class
definitions  of ``PublishingInformationSerializer`` and
``StockInformationSerializer`` nested serializers.

Then we define our (main) ``BookSerializer`` class, which is going to be
used as a ``serializer_class`` of the ``BookViewSet``. We inherit the
``BookSerializer`` from
``rest_framework_tricks.serializers.HyperlinkedModelSerializer``
instead of the one of the Django REST framework. There's also a
``rest_framework_tricks.serializers.ModelSerializer`` available.

Required imports
^^^^^^^^^^^^^^^^

.. code-block:: python

    from rest_framework import serializers
    from rest_framework_tricks.serializers import (
        HyperlinkedModelSerializer,
    )

    from .models import Book

Defining the serializers
^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

    If you get validation errors about null-values, add ``allow_null=True``
    next to the ``required=False`` for serializer field definitions.

**Nested serializer**

.. code-block:: python

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
            # Note, that this should be set to True to identify that
            # this serializer is going to be used as `NestedProxyField`.
            nested_proxy_field = True

**Nested serializer**

.. code-block:: python

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
            # Note, that this should be set to True to identify that
            # this serializer is going to be used as `NestedProxyField`.
            nested_proxy_field = True

**Main serializer to be used in the ViewSet**

.. code-block:: python

    # Note, that we are importing the ``HyperlinkedModelSerializer`` from
    # the `rest_framework_tricks.serializers`. Names of the serializers
    # should match the names of model properties set with ``NestedProxyField``
    # fields.
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

Sample ViewSet
~~~~~~~~~~~~~~

Absolutely no variations from standard implementation here.

Required imports
^^^^^^^^^^^^^^^^

.. code-block:: python

    from rest_framework.viewsets import ModelViewSet
    from rest_framework.permissions import AllowAny

    from .models import Book
    from .serializers import BookSerializer

ViewSet definition
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    class BookViewSet(ModelViewSet):
        """Book ViewSet."""

        queryset = Book.objects.all()
        serializer_class = BookSerializer
        permission_classes = [AllowAny]

Sample OPTIONS call
^^^^^^^^^^^^^^^^^^^

.. code-block:: text

    OPTIONS /books/api/books/
    HTTP 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

.. code-block:: javascript

    {
        "name": "Book List",
        "description": "Book ViewSet.",
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
                "title": {
                    "type": "string",
                    "required": true,
                    "read_only": false,
                    "label": "Title",
                    "max_length": 100
                },
                "description": {
                    "type": "string",
                    "required": false,
                    "read_only": false,
                    "label": "Description"
                },
                "summary": {
                    "type": "string",
                    "required": false,
                    "read_only": false,
                    "label": "Summary"
                },
                "publishing_information": {
                    "type": "nested object",
                    "required": false,
                    "read_only": false,
                    "label": "Publishing information",
                    "children": {
                        "publication_date": {
                            "type": "date",
                            "required": false,
                            "read_only": false,
                            "label": "Publication date"
                        },
                        "isbn": {
                            "type": "string",
                            "required": false,
                            "read_only": false,
                            "label": "Isbn"
                        },
                        "pages": {
                            "type": "integer",
                            "required": false,
                            "read_only": false,
                            "label": "Pages"
                        }
                    }
                },
                "stock_information": {
                    "type": "nested object",
                    "required": false,
                    "read_only": false,
                    "label": "Stock information",
                    "children": {
                        "stock_count": {
                            "type": "integer",
                            "required": false,
                            "read_only": false,
                            "label": "Stock count"
                        },
                        "price": {
                            "type": "decimal",
                            "required": true,
                            "read_only": false,
                            "label": "Price"
                        },
                        "state": {
                            "type": "choice",
                            "required": false,
                            "read_only": false,
                            "label": "State",
                            "choices": [
                                {
                                    "value": "published",
                                    "display_name": "Published"
                                },
                                {
                                    "value": "not_published",
                                    "display_name": "Not published"
                                },
                                {
                                    "value": "in_progress",
                                    "display_name": "In progress"
                                }
                            ]
                        }
                    }
                }
            }
        }
    }

Unlimited nesting depth
~~~~~~~~~~~~~~~~~~~~~~~

Unlimited nesting depth is supported.

Our imaginary ``Author`` model could consist of the following (non-relational)
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

In our REST API, we could split the Author serializer into parts using
nested serializers to have the following structure:

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

Our model would have to be defined as follows (see ``Advanced usage examples``
for complete model definition):

.. code-block:: python

    class Author(models.Model):
        """Author."""

        # ...

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

        # ...

See the `Advanced usage examples
<https://github.com/barseghyanartur/django-rest-framework-tricks/blob/master/ADVANCED_USAGE_EXAMPLES.rst#nested-serializers>`_
for complete example.

Demo
====
Run demo locally
----------------
In order to be able to quickly evaluate the ``django-rest-framework-tricks``,
a demo app (with a quick installer) has been created (works on Ubuntu/Debian,
may work on other Linux systems as well, although not guaranteed). Follow the
instructions below to have the demo running within a minute.

Grab and run the latest ``rest_framework_tricks_demo_installer.sh`` demo
installer:

.. code-block:: sh

    wget -O - https://raw.github.com/barseghyanartur/django-rest-framework-tricks/master/examples/rest_framework_tricks_demo_installer.sh | bash

Open your browser and test the app.

.. code-block:: text

    http://127.0.0.1:8001/books/api/

Testing
=======

Project is covered with tests.

To test with all supported Python/Django versions type:

.. code-block:: sh

    tox

To test against specific environment, type:

.. code-block:: sh

    tox -e py36-django110

To test just your working environment type:

.. code-block:: sh

    ./runtests.py

To run a single test in your working environment type:

.. code-block:: sh

    ./runtests.py src/rest_framework_tricks/tests/test_nested_proxy_field.py

Or:

.. code-block:: sh

    ./manage.py test rest_framework_tricks.tests.test_nested_proxy_field

It's assumed that you have all the requirements installed. If not, first
install the test requirements:

.. code-block:: sh

    pip install -r examples/requirements/test.txt

Writing documentation
=====================

Keep the following hierarchy.

.. code-block:: text

    =====
    title
    =====

    header
    ======

    sub-header
    ----------

    sub-sub-header
    ~~~~~~~~~~~~~~

    sub-sub-sub-header
    ^^^^^^^^^^^^^^^^^^

    sub-sub-sub-sub-header
    ++++++++++++++++++++++

    sub-sub-sub-sub-sub-header
    **************************

License
=======

GPL 2.0/LGPL 2.1

Support
=======

For any issues contact me at the e-mail given in the `Author`_ section.

Author
======

Artur Barseghyan <artur.barseghyan@gmail.com>

Project documentation
=====================
Contents:

.. contents:: Table of Contents

.. toctree::
   :maxdepth: 20

   index
   advanced_usage_examples
   changelog
   package

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

