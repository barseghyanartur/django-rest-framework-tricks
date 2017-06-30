from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .models import Book, Publisher
from .serializers import BookSerializer, PublisherSerializer

__all__ = (
    'BookViewSet',
    'PublisherViewSet',
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
