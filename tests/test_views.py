"""Views testing module."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from freelance.models import Developer, Position


def create_view_test_user(page_url, page_name, template, auth=True):
    """
    Decorate function for test creating.

    Args:
        page_url: str - url;
        page_name: str - name of the page, that will be requested;
        template: template;
        auth: bool - is or isn't user authorized.

    Returns:
        return: function decarator.
    """
    def test_auth(self):
        """
        Test authorized users.

        Args:
            self: self params.
        """
        client = APIClient()
        if auth:
            user = User.objects.create(username='dsjfbh', password='asdasd')
            position = Position.objects.create(name='deceloper')
            Developer.objects.create(developer=user, position=position)
            client.force_login(user)

        self.assertEqual(client.get(page_url).status_code, status.HTTP_200_OK)

        self.assertEqual(client.get(reverse(page_name)).status_code, status.HTTP_200_OK)

        response = client.get(page_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, template)

        client.logout()

    return test_auth


def unauthorized_view_test(page_url):
    """
    Test unauthorized user function decorator.

    Args:
        page_url: str - url.

    Returns:
        return: function.
    """
    def test_no_auth(self):
        """
        Test not authorized users.

        Args:
            self: self params.
        """
        client = APIClient()
        self.assertEqual(client.get(page_url).status_code, status.HTTP_302_FOUND)

    return test_no_auth


pages_attrs = (
    ('/dev-tasks/', 'dev_tasks', 'tasks.html'),
    ('/my-tasks/', 'my_tasks', 'tasks.html'),
)

casual_pages = (
    ('', 'main_page', 'main.html'),
    ('/register/', 'register', 'registration/register.html'),
    ('/login/', 'login', 'registration/login.html'),
)

auth_test_methods = {
    f'test_{attrs[1]}': create_view_test_user(*attrs) for attrs in pages_attrs
}
TestAuth = type('TestAuth', (TestCase,), auth_test_methods)

casual_methods = {
    f'test_noauth_{attrs[1]}': create_view_test_user(*attrs, auth=False) for attrs in casual_pages
}
casual_methods.update(
    {
        f'test_auth_{attrs[1]}': create_view_test_user(*attrs) for attrs in casual_pages
    },
)
TestCasualNoAuth = type('TestCasualNoAuth', (TestCase,), casual_methods)

no_auth_test_methods = {
    f'test_{attrs[1]}': unauthorized_view_test(attrs[0]) for attrs in pages_attrs
}
TestNoAuth = type('TestNoAuth', (TestCase,), no_auth_test_methods)
