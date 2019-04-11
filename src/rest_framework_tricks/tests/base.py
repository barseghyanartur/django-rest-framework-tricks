"""
Base tests.
"""

import logging

from django.test import TestCase
from rest_framework.test import APITestCase
from faker import Faker

import pytest

import factories

__title__ = 'rest_framework_tricks.tests.base'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2017-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'BaseRestFrameworkTestCase',
    'BaseTestCase',
)

LOGGER = logging.getLogger(__name__)


@pytest.mark.django_db
class BaseRestFrameworkTestCase(APITestCase):
    """Base REST framework test case."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpTestData(cls):
        """Set up class."""

        # Create user
        cls.user = factories.TestUsernameSuperAdminUserFactory()

        # Fake data
        cls.faker = Faker()

    def authenticate(self):
        """Helper for logging the user in.

        :return:
        """
        self.client.login(
            username=factories.auth_user.TEST_USERNAME,
            password=factories.auth_user.TEST_PASSWORD
        )


@pytest.mark.django_db
class BaseTestCase(TestCase):
    """Base test case."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpTestData(cls):
        """Set up class."""

        # Create user
        cls.user = factories.TestUsernameSuperAdminUserFactory()

        # Fake data
        cls.faker = Faker()
