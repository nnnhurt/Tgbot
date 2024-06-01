"""Module views for app."""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import BasePermission

from .models import Button
from .serializers import ButtonSerializer


safe_methods = 'GET', 'HEAD', 'OPTIONS'
unsafe_methods = 'POST', 'DELETE', 'PUT'


class MyPermission(BasePermission):
    """
    Custom permission class for handling permissions.

    Attributes:
        safe_methods (list): List of HTTP methods considered safe.
        unsafe_methods (list): List of HTTP methods considered unsafe.
    """

    def has_permission(self, request, _):
        """
        Check if the user has permission to perform the requested action.

        Args:
            request: The HTTP request object.
            _: Unused parameter.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        if request.method in safe_methods:
            return bool(request.user and request.user.is_authenticated)
        elif request.method in unsafe_methods:
            return bool(request.user and request.user.is_superuser)
        return False


class MasterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing masters.

    Attributes:
        queryset: The queryset of masters.
        serializer_class: The serializer class for masters.
        permission_classes: The permission classes for the viewset.
        authentication_classes: The authentication classes for the viewset.
    """

    queryset = Button.objects.filter(parent_id=None)
    serializer_class = ButtonSerializer
    permission_classes = [MyPermission]
    authentication_classes = [TokenAuthentication]


def create_viewset(model_class, serializer):
    """
    Create a custom ViewSet for a given model and serializer.

    Args:
        model_class: The model class to create the ViewSet for.
        serializer: The serializer class to use for the ViewSet.

    Returns:
        ViewSet: A custom ViewSet class for the specified model and serializer.
    """
    class ViewSet(viewsets.ModelViewSet):
        """
        Custom ViewSet for managing instances of a model.

        Attributes:
            queryset: The queryset of instances.
            serializer_class: The serializer class for instances.
            permission_classes: The permission classes for the viewset.
            authentication_classes: The authentication classes for the viewset.
        """

        queryset = model_class.objects.all()
        serializer_class = serializer
        permission_classes = [MyPermission]
        authentication_classes = [TokenAuthentication]

    return ViewSet


ButtonViewSet = create_viewset(Button, ButtonSerializer)
