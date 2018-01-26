"""
View sets.
"""

import django_filters

from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .filters import CustomStatusFilter
from .models import (
    Author,
    AuthorProxy,
    Book,
    BookProxy,
    Profile,
    Publisher,
)
from .serializers import (
    AuthorSerializer,
    AuthorProxySerializer,
    BookSerializer,
    BookProxySerializer,
    PublisherSerializer,
    ProfileSerializer,
)

__all__ = (
    'AuthorViewSet',
    'AuthorProxyViewSet',
    'BookViewSet',
    'BookProxyViewSet',
    'PublisherViewSet',
    'ProfileViewSet',
)


class BookViewSet(ModelViewSet):
    """Book ViewSet."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class BookProxyViewSet(ModelViewSet):
    """Book proxy ViewSet."""

    queryset = BookProxy.objects.all()
    serializer_class = BookProxySerializer
    permission_classes = [AllowAny]
    filter_class = CustomStatusFilter
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        filters.OrderingFilter,
    )
    ordering_fields = ('id', 'publisher__name',)


class PublisherViewSet(ModelViewSet):
    """Publisher ViewSet."""

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [AllowAny]


class AuthorViewSet(ModelViewSet):
    """Author ViewSet."""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]


class AuthorProxyViewSet(ModelViewSet):
    """AuthorProxy ViewSet."""

    queryset = AuthorProxy.objects.all()
    serializer_class = AuthorProxySerializer
    permission_classes = [AllowAny]


class ProfileViewSet(ModelViewSet):
    """Profile ViewSet."""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]
