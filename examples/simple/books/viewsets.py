from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .models import (
    Author,
    AuthorProxy,
    Book,
    Profile,
    Publisher,
)
from .serializers import (
    AuthorSerializer,
    AuthorProxySerializer,
    BookSerializer,
    PublisherSerializer,
    ProfileSerializer,
)

__all__ = (
    'AuthorViewSet',
    'AuthorProxyViewSet',
    'BookViewSet',
    'PublisherViewSet',
    'ProfileViewSet',
)


class BookViewSet(ModelViewSet):
    """Book ViewSet."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


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
