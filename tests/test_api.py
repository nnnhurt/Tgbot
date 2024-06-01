"""Module for test api."""
from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from app.models import Button


MOCK_DATA = datetime(2049, 11, 25)


def create_api_test(model_class, url, creation_attrs):
    """
    Create API test case class.

    Args:
        model_class: The model class being tested.
        url (str): The URL endpoint for the API.
        creation_attrs (dict): Attributes for creating test objects.

    Returns:
        TestCase: A test case class for API testing.
    """
    class ApiTest(TestCase):
        """Test case class for API testing."""

        def setUp(self):
            """
            Set up test case.

            Initializes API client and creates users and tokens for testing.
            """
            self.client = APIClient()
            # users
            self.user = User(username='user', password='user')
            self.superuser = User(
                username='admin', password='admin', is_superuser=True)
            # tokens for users
            self.user_token = Token(user=self.user)
            self.superuser_token = Token(user=self.superuser)

        def api_methods(
                self, user: User, token: Token,
                post_exp: int, put_exp: int, delete_exp: int,
                patch_exp: int, post_fail_exp: int,
        ):
            self.client.force_authenticate(user=user, token=token)

            # create model object
            self.created_id = model_class.objects.create(**creation_attrs).id
            instance_url = f'{url}{self.created_id}/'

            # GET all
            self.assertEqual(self.client.options(
                url).status_code, status.HTTP_200_OK)

            # HEAD all
            self.assertEqual(self.client.head(
                url).status_code, status.HTTP_200_OK)

            # OPTIONS all
            self.assertEqual(self.client.get(
                url).status_code, status.HTTP_200_OK)

            # GET instance
            self.assertEqual(self.client.get(
                instance_url).status_code, status.HTTP_200_OK)

            # OPTIONS instance
            self.assertEqual(self.client.get(
                instance_url).status_code, status.HTTP_200_OK)

            # POST
            self.assertEqual(self.client.post(
                url, creation_attrs).status_code, post_exp)

            # POST FAILURE
            creation_attrs_fail = creation_attrs.update({'created': MOCK_DATA})
            self.assertEqual(self.client.post(
                url, creation_attrs_fail).status_code, post_fail_exp)
            # PATCH
            self.assertEqual(self.client.patch(
                url, creation_attrs).status_code, patch_exp)

            # PUT
            self.assertEqual(self.client.put(
                instance_url, creation_attrs).status_code, put_exp)

            # DELETE
            self.assertEqual(self.client.delete(
                instance_url).status_code, delete_exp)

        def test_superuser(self):
            self.api_methods(
                self.superuser, self.superuser_token,
                status.HTTP_201_CREATED,
                status.HTTP_200_OK,
                status.HTTP_204_NO_CONTENT,
                status.HTTP_403_FORBIDDEN,
                status.HTTP_400_BAD_REQUEST,
            )

        def test_user(self):
            self.api_methods(
                self.user, self.user_token,
                status.HTTP_403_FORBIDDEN,
                status.HTTP_403_FORBIDDEN,
                status.HTTP_403_FORBIDDEN,
                status.HTTP_403_FORBIDDEN,
                status.HTTP_403_FORBIDDEN,
            )

    return ApiTest


GamesApiTest = create_api_test(
    Button, '/api/buttons/', {'title': 'Z', 'description': 'what'})
