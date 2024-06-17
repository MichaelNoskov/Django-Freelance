"""API tests module."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from freelance import models

NAME = 'name'
CREATED = 'created'
OWNER = 'owner'
SLESH = '/'


def create_apitest(
    model_class,
    model_url,
    creation_attrs,
):
    """
    Create tests.

    Args:
        model_class: model;
        model_url: str url for sending requests;
        creation_attrs: tests attrs.

    Returns:
        return: APITest testing class
    """

    class APITest(TestCase):
        """Test API requests."""

        _user_creds = {'username': 'abc', 'password': 'abc'}
        _superuser_creds = {
            'username': 'def',
            'password': 'def',
            'is_staff': True,
        }

        def setUp(self):
            """Set up test data for API."""
            self.client = APIClient()
            self.user = User.objects.create(**self._user_creds)
            self.user_token = Token(user=self.user)
            self.superuser = User.objects.create(**self._superuser_creds)
            self.superuser_token = Token(user=self.superuser)

        def test_categories_post(self):
            """Test post categorial objects."""
            self.client.force_authenticate(user=self.superuser, token=self.superuser_token)

            # POST
            response = self.client.post(model_url, creation_attrs)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_categories_put_delete(self):
            """Test put and delete categorial objects."""
            self.client.force_authenticate(user=self.superuser, token=self.superuser_token)

            # creating object for changes
            created = model_class.objects.create(**creation_attrs)
            url = model_url + str(created.id) + SLESH

            # PUT
            response = self.client.put(url, creation_attrs)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # DELETE
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        def test_unsuccessful_task(self):
            """Test unsuccessful for Task model."""
            self.client.force_authenticate(user=self.superuser, token=self.superuser_token)
            url = '/api/tasks/'

            # POST
            task_status = models.Status.objects.create(**{NAME: CREATED})
            task_creation_attrs = {
                NAME: 'some task',
                'description': 'its a task',
                OWNER: self.superuser.id,
                'status': task_status.id,
                CREATED: '2083-12-12',
            }

            # task in the past
            response = self.client.post(url, task_creation_attrs)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

            # PUT

            created = models.Task.objects.create(
                name='some task',
                description='its a task',
                owner=self.superuser,
                status=task_status,
                created=timezone.now(),
            )
            url = url + str(created.id) + SLESH

            # not success test (task in the future)
            response = self.client.put(url, task_creation_attrs)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        def test_task(self):
            """Test Task model."""
            self.client.force_authenticate(user=self.superuser, token=self.superuser_token)
            url = '/api/tasks/'

            # POST
            task_status = models.Status.objects.create(**{NAME: CREATED})

            task_creation_attrs = {
                NAME: 'some task',
                'description': 'its a task',
                OWNER: self.superuser.id,
                'status': task_status.id,
                CREATED: '2023-12-12',
            }

            # success test
            response = self.client.post(url, task_creation_attrs)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            created = models.Task.objects.create(
                name='strange task',
                description='this is a task',
                owner=self.superuser,
                status=task_status,
                created=timezone.now(),
            )

            url = url + str(created.id) + SLESH

            # PUT
            response = self.client.put(url, task_creation_attrs)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # DELETE
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        def test_comment(self):
            """Test Comment model."""
            self.client.force_authenticate(user=self.superuser, token=self.superuser_token)

            task_status = models.Status.objects.create(**{NAME: CREATED})
            task = models.Task.objects.create(
                **{
                    NAME: 'easy task',
                    'description': 'task for children',
                    OWNER: self.superuser,
                    'status': task_status,
                    CREATED: timezone.now(),
                },
            )

            position = models.Position.objects.create(**{NAME: 'student'})

            dev = models.Developer.objects.create(
                developer=self.superuser, position=position,
            )

            url = '/api/comments/'

            # POST

            # successful request
            response = self.client.post(
                url,
                {
                    'comment_content': 'it is a very bad job',
                    'task': task.id,
                    OWNER: dev.id,
                },
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # PUT
            created = models.Comment.objects.create(**{
                'comment_content': 'it is a very bad job',
                'task': task,
                OWNER: dev,
            })

            url = url + str(created.id) + SLESH

            response = self.client.put(
                url,
                {
                    'comment_content': 'it is a very bad job',
                    'task': task.id,
                    OWNER: dev.id,
                },
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # DELETE
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    return APITest


StatusApiTest = create_apitest(models.Status, '/api/statuses/', {NAME: CREATED})
PositionApiTest = create_apitest(models.Position, '/api/positions/', {NAME: 'student'})
