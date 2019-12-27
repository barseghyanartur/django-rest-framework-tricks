"""
Urls.
"""

from django.conf.urls import url, include

import rest_framework
from rest_framework.routers import DefaultRouter

from .views import (
    AddAuthorsToBookView,
    AuthorListView,
    AuthorListJSONView,
    AuthorListValuesView,
    AuthorListValuesWithCountsView,
    AuthorListWithCountsView,
    CreateAuthorsView,
    BookListView,
    BookListValuesView,
    BookListWithCountsView,
    PublisherIDsView,
    PublisherListView,
    UpdateBooksView,
    IndexView,
)
from .viewsets import (
    AuthorViewSet,
    AuthorProxyViewSet,
    BookViewSet,
    BookProxyViewSet,
    BookProxy2ViewSet,
    ProfileViewSet,
    PublisherViewSet,
)

__all__ = ('urlpatterns',)

BASENAME = 'basename'

try:
    drf_version = rest_framework.__version__.split('.')[:2]
    drf_version = tuple(int(_i) for _i in drf_version)
    if drf_version < (3, 9):
        BASENAME = 'base_name'
except:
    pass

router = DefaultRouter()

router.register(
    r'books',
    BookViewSet,
    **{BASENAME: 'book'}
)

router.register(
    r'proxy-books',
    BookProxyViewSet,
    **{BASENAME: 'bookproxy'}
)

router.register(
    r'proxy2-books',
    BookProxy2ViewSet,
    **{BASENAME: 'bookproxy2'}
)

router.register(
    r'publishers',
    PublisherViewSet,
    **{BASENAME: 'publisher'}
)

router.register(
    r'profiles',
    ProfileViewSet,
    **{BASENAME: 'profile'}
)

router.register(
    r'authors',
    AuthorViewSet,
    **{BASENAME: 'author'}
)

router.register(
    r'proxy-authors',
    AuthorProxyViewSet,
    **{BASENAME: 'authorproxy'}
)

urlpatterns = [
    url(r'^api/', include(router.urls)),

    # Authors list
    url(r'^authors/$', AuthorListView.as_view(), name='books.authors'),

    # Authors list (more efficient)
    url(r'^authors-values/$',
        AuthorListValuesView.as_view(),
        name='books.authors_values'),

    # Authors list (with counts)
    url(r'^authors-with-counts/$',
        AuthorListWithCountsView.as_view(),
        name='books.authors_with_counts'),

    # Authors list (values with counts)
    url(r'^authors-values-with-counts/$',
        AuthorListValuesWithCountsView.as_view(),
        name='books.authors_values_with_counts'),

    # Authors list in JSON format
    url(r'^authors-json/$',
        AuthorListJSONView.as_view(),
        name='books.authors_json'),

    # Books list
    url(r'^books/$', BookListView.as_view(), name='books.books'),

    # Books list (with counts)
    url(r'^books-with-counts/$',
        BookListWithCountsView.as_view(),
        name='books.books_with_counts'),

    # Books list (more efficient)
    url(r'^books-values/$',
        view=BookListValuesView.as_view(),
        name='books.books_values'),

    # Publishers list
    url(r'^publishers/$',
        PublisherListView.as_view(),
        name='books.publishers'),

    # Publisher IDs
    url(r'^publisher-ids/$',
        PublisherIDsView.as_view(),
        name='books.publisher_ids'),

    # Create authors view
    url(r'^create-authors/$',
        CreateAuthorsView.as_view(),
        name='books.create_authors'),

    # Add authors to a book view
    url(r'^add-authors-to-book/$',
        AddAuthorsToBookView.as_view(),
        name='books.add_authors_to_book'),

    # Update books view
    url(r'^update-books/$',
        UpdateBooksView.as_view(),
        name='books.update_books'),

    # Index view
    url(r'^$', IndexView.as_view(), name='books.index'),
]
