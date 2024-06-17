"""Permissions testing module."""

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from freelance.permissions import AdminOrReadOnlyPermission, UserPermission


class AdminPermissionTest(TestCase):
    """Tests user admin permission."""

    def setUp(self):
        """Set up test data for user admin permission."""
        self.factory = RequestFactory()
        self.permission = AdminOrReadOnlyPermission()
        self.view = None
        self.user = User.objects.create_user(
            username='asdasd',
            password='qwsljkas',
        )

    def test_has_object_permission(self):
        """Test has object permission."""
        request = self.factory.get('/')
        request.user = self.user
        objc = None
        self.assertTrue(self.permission.has_object_permission(request, self.view, objc))


class DefaultUserPermissionTest(TestCase):
    """Tests user admin permission."""

    def setUp(self):
        """Set up test data for user admin permission."""
        self.factory = RequestFactory()
        self.permission = UserPermission()
        self.view = None
        self.user = User.objects.create_user(
            username='htryuykui',
            password='sdfgdfbrt4',
        )

    def test_has_object_permission(self):
        """Test has object permission."""
        request = self.factory.get('/')
        request.user = self.user
        objc = None
        self.assertTrue(self.permission.has_object_permission(request, self.view, objc))
