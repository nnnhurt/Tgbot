"""Module for test on methods."""
from datetime import datetime, timezone

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from app.models import Button, check_date_created


MOCK_DATA = datetime(2049, 11, 25, tzinfo=timezone.utc)


class ApiTest(TestCase):
    """Test case class for API testing."""

    def setUp(self):
        """
        Set up test case.

        Initializes API client and creates users and tokens for testing.
        """
        self.client = APIClient()
        self.user = User(username='user', password='user')
        self.superuser = User(
            username='admin', password='admin', is_superuser=True)
        self.user_token = Token(user=self.user)
        self.superuser_token = Token(user=self.superuser)

    def test_data(self) -> None:
        """
        Test data validation.

        Asserts that the data validation function raises ValidationError
        for mock data.
        """
        with self.assertRaises(ValidationError):
            check_date_created(MOCK_DATA)

    def test_string(self) -> None:
        """
        Test string representation.

        Asserts that the string representation of a Button object
        is equal to its title.
        """
        button = Button.objects.create(
            title='test_button', description='iejgieiwngj')
        self.assertEqual(str(button), button.title)
