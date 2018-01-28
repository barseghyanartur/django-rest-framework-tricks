"""
View sets.
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from rest_framework_tricks.filters import OrderingFilter

from .models import (
    Author,
    AuthorProxy,
    Book,
    BookProxy,
    BookProxy2,
    Profile,
    Publisher,
)
from .serializers import (
    AuthorSerializer,
    AuthorProxySerializer,
    BookSerializer,
    BookProxySerializer,
    BookProxy2Serializer,
    PublisherSerializer,
    ProfileSerializer,
)

__all__ = (
    'AuthorViewSet',
    'AuthorProxyViewSet',
    'BookViewSet',
    'BookProxyViewSet',
    'BookProxy2ViewSet',
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

    queryset = BookProxy.objects.all().select_related('publisher')
    serializer_class = BookProxySerializer
    permission_classes = [AllowAny]
    filter_backends = (
        OrderingFilter,
    )
    ordering_fields = {
        'id': 'id',
        'city': 'publisher__city',
    }
    ordering = ('id',)


class BookProxy2ViewSet(ModelViewSet):
    """Book proxy 2 ViewSet."""

    queryset = BookProxy2.objects.all().select_related('publisher')
    serializer_class = BookProxy2Serializer
    permission_classes = [AllowAny]
    filter_backends = (
        OrderingFilter,
    )
    ordering_fields = ('id',)
    ordering = ('id',)


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
