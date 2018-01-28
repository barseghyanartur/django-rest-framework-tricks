"""
Test OrderingFilter.
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
__copyright__ = '2017-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TestOrderingFilter',
)


@pytest.mark.django_db
class TestOrderingFilter(BaseRestFrameworkTestCase):
    """Test OrderingFilter."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up."""
        super(TestOrderingFilter, cls).setUpClass()

        cls.bookproxy_listing_url = reverse('bookproxy-list', kwargs={})
        cls.bookproxy2_listing_url = reverse('bookproxy2-list', kwargs={})
        cls.books = factories.BookFactory.create_batch(10)

    def _test_ordering(self, descending=False):
        """Test ordering.

        :param descending:
        :return:
        """
        response = self.client.get(
            self.bookproxy_listing_url,
            {'ordering': '-city' if descending else 'city'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = []
        for item in response.data['results']:
            data.append(item['city'] if item['city'] else '')

        sorted_data = sorted(data)
        if descending:
            sorted_data = list(reversed(sorted_data))

        self.assertEqual(data, sorted_data)

    def test_ordering(self):
        """Test ordering (ascending).

        :return:
        """
        return self._test_ordering()

    def test_ordering_descending(self):
        """Test ordering (descending).

        :return:
        """
        return self._test_ordering(descending=True)

    def _test_standard_ordering(self, descending=False):
        """Test standard ordering.

        :param descending:
        :return:
        """
        response = self.client.get(
            self.bookproxy2_listing_url,
            {'ordering': '-id' if descending else 'id'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = []
        for item in response.data['results']:
            data.append(item['id'] if item['id'] else '')

        sorted_data = sorted(data)
        if descending:
            sorted_data = list(reversed(sorted_data))

        self.assertEqual(data, sorted_data)

    def test_standard_ordering(self):
        """Test standard ordering (ascending).

        :return:
        """
        return self._test_standard_ordering()

    def test_standard_ordering_descending(self):
        """Test standard ordering (descending).

        :return:
        """
        return self._test_standard_ordering(descending=True)

    def test_standard_no_ordering(self):
        """Test standard no ordering.

        :return:
        """
        response = self.client.get(
            self.bookproxy_listing_url,
            {},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = []
        for item in response.data['results']:
            data.append(item['id'] if item['id'] else '')

        sorted_data = sorted(data)

        self.assertEqual(data, sorted_data)


if __name__ == '__main__':
    unittest.main()
