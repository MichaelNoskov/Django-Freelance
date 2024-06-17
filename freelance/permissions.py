"""This module contains different access permissions."""

from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    """Default users's permission."""

    def has_permission(self, request, view):
        """
        Check if user was authenticate.

        Args:
            request: A request object;
            view: view.

        Returns:
            str: A boolen access information.
        """
        return request.user.is_authenticated

    def has_object_permission(self, request, view, m_object):
        """
        Check if user is a staff.

        Args:
            request: A request object;
            view: view;
            m_object: model object.

        Returns:
            str: A boolen access information.
        """
        if request.user.is_authenticated and request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or m_object.owner == request.user


class AdminOrReadOnlyPermission(permissions.BasePermission):
    """Admin's permission."""

    def has_permission(self, request, view):
        """
        Check if user was authenticate.

        Args:
            request: A request object;
            view: view.

        Returns:
            str: A boolen access information.
        """
        if request.user.is_authenticated and request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, m_object):
        """
        Check if user is a staff.

        Args:
            request: A request object;
            view: view;
            m_object: model object.

        Returns:
            str: A boolen access information.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
