"""
Test OrderingFilter.
"""
import unittest

from django.urls import reverse
import pytest
from rest_framework import status

import factories

from .base import BaseRestFrameworkTestCase

__title__ = "rest_framework_tricks.tests.test_nested_proxy_field"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = ("TestOrderingFilter",)


@pytest.mark.django_db
class TestOrderingFilter(BaseRestFrameworkTestCase):
    """Test OrderingFilter."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up."""
        super(TestOrderingFilter, cls).setUpClass()

        cls.bookproxy_listing_url = reverse("bookproxy-list", kwargs={})
        cls.bookproxy2_listing_url = reverse("bookproxy2-list", kwargs={})
        cls.books = factories.BookFactory.create_batch(10)

    def _test_ordering(self, descending=False):
        """Test ordering.

        :param descending:
        :return:
        """
        response = self.client.get(
            self.bookproxy_listing_url,
            {"ordering": "-city" if descending else "city"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = []
        for item in response.data["results"]:
            data.append(item["city"] if item["city"] else "")

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
            {"ordering": "-id" if descending else "id"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = []
        for item in response.data["results"]:
            data.append(item["id"] if item["id"] else "")

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
        response = self.client.get(self.bookproxy_listing_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = []
        for item in response.data["results"]:
            data.append(item["id"] if item["id"] else "")

        sorted_data = sorted(data)

        self.assertEqual(data, sorted_data)

    def _test_ordering_list(self, descending=False):
        """Test ordering list.

        :param descending:
        :return:
        """
        response = self.client.get(
            self.bookproxy_listing_url,
            {"ordering": "-status" if descending else "status"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = []
        data_2 = []
        for item in response.data["results"]:
            _state = item["state"] if item["state"] else ""
            _pub_date = (
                item["publishing_information"]["publication_date"]
                if item["publishing_information"]["publication_date"]
                else ""
            )
            data.append(_state)
            data_2.append("{} {}".format(_state, _pub_date))

        sorted_data = sorted(data)
        sorted_data_2 = sorted(data_2)
        if descending:
            sorted_data = list(reversed(sorted_data))
            sorted_data_2 = list(reversed(sorted_data_2))

        self.assertEqual(data, sorted_data)
        self.assertEqual(data_2, sorted_data_2)

    def test_ordering_list(self):
        """Test ordering list (ascending).

        :return:
        """
        return self._test_ordering_list()

    def test_ordering_list_descending(self):
        """Test ordering list (descending).

        :return:
        """
        return self._test_ordering_list(descending=True)
