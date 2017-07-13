"""
Test NestedProxyField.
"""

from __future__ import absolute_import

from decimal import Decimal

import unittest

from nine.versions import DJANGO_GTE_1_10

import pytest

from rest_framework import status

import factories

from .base import BaseRestFrameworkTestCase

if DJANGO_GTE_1_10:
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

__title__ = 'rest_framework_tricks.tests.test_nested_proxy_field'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestNestedProxyFieldCreateAction',
    'TestNestedProxyFieldUpdateAction',
)


@pytest.mark.django_db
class TestNestedProxyFieldCreateAction(BaseRestFrameworkTestCase):
    """Test NestedProxyField - update action."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up."""
        super(TestNestedProxyFieldCreateAction, cls).setUpClass()

        cls.book_listing_url = reverse('book-list', kwargs={})
        cls.publisher_listing_url = reverse('publisher-list', kwargs={})
        cls.author_listing_url = reverse('author-list', kwargs={})
        cls.profile_listing_url = reverse('profile-list', kwargs={})
        cls.proxy_author_listing_url = reverse('authorproxy-list', kwargs={})

    def _nested_proxy_field_hyperlinked_model_serializer(self, url=None):
        """Test NestedProxyField and HyperlinkedModelSerializer."""
        data = {
            'title': self.faker.text(max_nb_chars=100),
            'description': self.faker.text(),
            'summary': self.faker.text(),
            'publishing_information': {
                'publication_date': self.faker.date(),
                'isbn': self.faker.isbn10(),
                'pages': self.faker.pyint()
            },
            'stock_information': {
                'stock_count': self.faker.pyint(),
                'price': self.faker.pyint(),
                'state': 'published'
            }
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for __key in ('title', 'summary', 'description'):
            self.assertEqual(response.data.get(__key), data.get(__key))

        for __key in ('publication_date', 'isbn', 'pages'):
            self.assertEqual(
                response.data['publishing_information'].get(__key),
                data['publishing_information'].get(__key)
            )

        for __key in ('stock_count', 'state'):
            self.assertEqual(
                response.data['stock_information'].get(__key),
                data['stock_information'].get(__key)
            )
        self.assertEqual(
            Decimal(response.data['stock_information'].get('price')),
            Decimal(data['stock_information'].get('price'))
        )

    def test_nested_proxy_field_hyperlinked_model_serializer(self):
        """Test NestedProxyField and HyperlinkedModelSerializer."""
        self._nested_proxy_field_hyperlinked_model_serializer(
            self.book_listing_url
        )

    def _nested_proxy_field_model_serializer(self, url=None):
        """Test NestedProxyField and ModelSerializer."""
        data = {
            'name': self.faker.text(max_nb_chars=30),
            'info': self.faker.text(),
            'website': self.faker.url(),
            'address_information': {
                'address': self.faker.address(),
                'city': self.faker.city(),
                'state_province': self.faker.state(),
                'country': self.faker.country()
            }
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for __key in ('name', 'info', 'website'):
            self.assertEqual(response.data.get(__key), data.get(__key))

        for __key in ('address', 'city', 'state_province', 'country'):
            self.assertEqual(
                response.data['address_information'].get(__key),
                data['address_information'].get(__key)
            )

    def test_nested_proxy_field_model_serializer(self):
        """Test NestedProxyField and ModelSerializer."""
        self._nested_proxy_field_model_serializer(
            self.publisher_listing_url
        )

    def _nested_proxy_field_model_serializer_depth(self, url=None):
        """Test NestedProxyField and ModelSerializer with more depth."""
        data = {
            'salutation': self.faker.text(max_nb_chars=10),
            'name': self.faker.name(),
            'birth_date': self.faker.date(),
            'biography': self.faker.text(),
            'contact_information': {
                'personal_contact_information': {
                    'email': self.faker.email(),
                    'phone_number': self.faker.phone_number(),
                    'website': self.faker.url(),
                },
                'business_contact_information': {
                    'company': self.faker.company(),
                    'company_email': self.faker.email(),
                    'company_phone_number': self.faker.phone_number(),
                    'company_website': self.faker.url()
                }
            }
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for __key in ('salutation', 'name', 'biography'):
            self.assertEqual(response.data.get(__key), data.get(__key))

        for __key in ('email', 'phone_number', 'website'):
            self.assertEqual(
                response.data['contact_information']
                             ['personal_contact_information'].get(__key),
                data['contact_information']
                    ['personal_contact_information'].get(__key)
            )

        for __key in ('company',
                      'company_email',
                      'company_phone_number',
                      'company_website'):
            self.assertEqual(
                response.data['contact_information']
                             ['business_contact_information'].get(__key),
                data['contact_information']
                    ['business_contact_information'].get(__key)
            )

    def test_nested_proxy_field_model_serializer_depth(self):
        """Test NestedProxyField and ModelSerializer with more depth."""
        self._nested_proxy_field_model_serializer_depth(
            self.author_listing_url
        )

    def test_another_nested_proxy_field_model_serializer_depth(self):
        """Test NestedProxyField and ModelSerializer with more depth."""
        self._nested_proxy_field_model_serializer_depth(
            self.proxy_author_listing_url
        )

    def _nested_proxy_field_model_serializer_more_depth(self, url=None):
        """Test NestedProxyField and ModelSerializer with more depth."""
        data = {
            'information': {
                'data': {
                    'personal_information': {
                        'salutation': self.faker.text(max_nb_chars=10),
                        'first_name': self.faker.first_name(),
                        'last_name': self.faker.last_name(),
                        'birth_date': self.faker.date(),
                        'biography': self.faker.text(),
                    },
                    'contact_information': {
                        'personal_contact_information': {
                            'email': self.faker.email(),
                            'phone_number': self.faker.phone_number(),
                            'website': self.faker.url(),
                        },
                        'business_contact_information': {
                            'company': self.faker.company(),
                            'company_email': self.faker.email(),
                            'company_phone_number': self.faker.phone_number(),
                            'company_website': self.faker.url()
                        }
                    },
                    'bank_information': {
                        'bank_name': self.faker.company(),
                        'bank_account_name': self.faker.name(),
                        'bank_account_number': self.faker.pystr(),
                    },
                }
            }
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for __key in ('salutation', 'first_name', 'last_name', 'biography'):
            self.assertEqual(
                response.data['information']
                             ['data']
                             ['personal_information'].get(__key),
                data['information']
                    ['data']
                    ['personal_information'].get(__key)
            )

        for __key in ('email', 'phone_number', 'website'):
            self.assertEqual(
                response.data['information']
                             ['data']
                             ['contact_information']
                             ['personal_contact_information'].get(__key),
                data['information']
                    ['data']
                    ['contact_information']
                    ['personal_contact_information'].get(__key)
            )

        for __key in ('company',
                      'company_email',
                      'company_phone_number',
                      'company_website'):
            self.assertEqual(
                response.data['information']
                             ['data']
                             ['contact_information']
                             ['business_contact_information'].get(__key),
                data['information']
                    ['data']
                    ['contact_information']
                    ['business_contact_information'].get(__key)
            )

        for __key in ('bank_name', 'bank_account_name', 'bank_account_number'):
            self.assertEqual(
                response.data['information']
                             ['data']
                             ['bank_information'].get(__key),
                data['information']
                    ['data']
                    ['bank_information'].get(__key)
            )

    def test_another_nested_proxy_field_model_serializer_more_depth(self):
        """Test NestedProxyField and ModelSerializer with more depth."""
        self._nested_proxy_field_model_serializer_more_depth(
            self.profile_listing_url
        )

    def _nested_proxy_field_model_serializer_missing_fields(self, url=None):
        """Test NestedProxyField and ModelSerializer with missing fields.

        In this case, the ``info`` field is missing.
        """
        data = {
            'name': self.faker.text(max_nb_chars=30),
            'website': self.faker.url(),
            'address_information': {
                'address': self.faker.address(),
                'city': self.faker.city(),
                'state_province': self.faker.state(),
                'country': self.faker.country()
            }
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for __key in ('name', 'website'):
            self.assertEqual(response.data.get(__key), data.get(__key))

        for __key in ('address', 'city', 'state_province', 'country'):
            self.assertEqual(
                response.data['address_information'].get(__key),
                data['address_information'].get(__key)
            )

    def test_nested_proxy_field_model_serializer_missing_fields(self):
        """Test NestedProxyField and ModelSerializer with missing fields."""
        self._nested_proxy_field_model_serializer_missing_fields(
            self.publisher_listing_url
        )


@pytest.mark.django_db
class TestNestedProxyFieldUpdateAction(BaseRestFrameworkTestCase):
    """Test NestedProxyField - update action."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up."""
        super(TestNestedProxyFieldUpdateAction, cls).setUpClass()

        cls.books = factories.BookFactory.create_batch(10)

        cls.book_detail_url = reverse(
            'book-detail',
            kwargs={'pk': cls.books[0].pk}
        )

        cls.publisher_detail_url = reverse(
            'publisher-detail',
            kwargs={'pk': cls.books[0].publisher.pk}
        )

        cls.author_detail_url = reverse(
            'author-detail',
            kwargs={'pk': cls.books[0].authors.first().pk}
        )

        cls.proxy_author_detail_url = reverse(
            'authorproxy-detail',
            kwargs={'pk': cls.books[0].authors.first().pk}
        )

    def _nested_proxy_field_hyperlinked_model_serializer(self, url=None):
        """Test NestedProxyField and HyperlinkedModelSerializer."""
        data = {
            'title': self.faker.sentence(nb_words=3, variable_nb_words=True),
            'description': self.faker.text(),
            'summary': self.faker.text(),
            'publishing_information': {
                'publication_date': self.faker.date(),
                'isbn': self.faker.isbn13(),
                'pages': self.faker.pyint()
            },
            'stock_information': {
                'stock_count': self.faker.pyint(),
                'price': self.faker.pyint(),
                'state': 'published'
            }
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for __key in ('title', 'summary', 'description'):
            self.assertEqual(response.data.get(__key), data.get(__key))

        for __key in ('publication_date', 'isbn', 'pages'):
            self.assertEqual(
                response.data['publishing_information'].get(__key),
                data['publishing_information'].get(__key)
            )

        for __key in ('stock_count', 'state'):
            self.assertEqual(
                response.data['stock_information'].get(__key),
                data['stock_information'].get(__key)
            )
        self.assertEqual(
            Decimal(response.data['stock_information'].get('price')),
            Decimal(data['stock_information'].get('price'))
        )

    def test_nested_proxy_field_hyperlinked_model_serializer(self):
        """Test NestedProxyField and HyperlinkedModelSerializer."""
        self._nested_proxy_field_hyperlinked_model_serializer(
            self.book_detail_url
        )

    def _nested_proxy_field_model_serializer(self, url=None):
        """Test NestedProxyField and ModelSerializer."""
        data = {
            'name': self.faker.sentence(nb_words=2, variable_nb_words=True),
            'info': self.faker.text(),
            'website': self.faker.url(),
            'address_information': {
                'address': self.faker.address(),
                'city': self.faker.city(),
                'state_province': self.faker.state(),
                'country': self.faker.country()
            }
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for __key in ('name', 'info', 'website'):
            self.assertEqual(response.data.get(__key), data.get(__key))

        for __key in ('address', 'city', 'state_province', 'country'):
            self.assertEqual(
                response.data['address_information'].get(__key),
                data['address_information'].get(__key)
            )

    def test_nested_proxy_field_model_serializer(self):
        """Test NestedProxyField and ModelSerializer."""
        self._nested_proxy_field_model_serializer(
            self.publisher_detail_url
        )

    def _nested_proxy_field_model_serializer_depth(self, url=None):
        """Test NestedProxyField and ModelSerializer with more depth."""
        data = {
            'salutation': self.faker.text(max_nb_chars=10),
            'name': self.faker.name(),
            'birth_date': self.faker.date(),
            'biography': self.faker.text(),
            'contact_information': {
                'personal_contact_information': {
                    'email': self.faker.email(),
                    'phone_number': self.faker.phone_number(),
                    'website': self.faker.url(),
                },
                'business_contact_information': {
                    'company': self.faker.company(),
                    'company_email': self.faker.email(),
                    'company_phone_number': self.faker.phone_number(),
                    'company_website': self.faker.url()
                }
            }
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for __key in ('salutation', 'name', 'biography'):
            self.assertEqual(response.data.get(__key), data.get(__key))

        for __key in ('email', 'phone_number', 'website'):
            self.assertEqual(
                response.data['contact_information']
                             ['personal_contact_information'].get(__key),
                data['contact_information']
                    ['personal_contact_information'].get(__key)
            )

        for __key in ('company',
                      'company_email',
                      'company_phone_number',
                      'company_website'):
            self.assertEqual(
                response.data['contact_information']
                             ['business_contact_information'].get(__key),
                data['contact_information']
                    ['business_contact_information'].get(__key)
            )

    def test_nested_proxy_field_model_serializer_depth(self):
        """Test NestedProxyField and ModelSerializer with more depth."""
        self._nested_proxy_field_model_serializer_depth(
            self.author_detail_url
        )

    def test_another_nested_proxy_field_model_serializer_depth(self):
        """Test NestedProxyField and ModelSerializer with more depth."""
        self._nested_proxy_field_model_serializer_depth(
            self.proxy_author_detail_url
        )


if __name__ == '__main__':
    unittest.main()
