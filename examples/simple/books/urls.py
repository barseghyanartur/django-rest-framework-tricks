"""
Urls.
"""

from django.conf.urls import url, include

from rest_framework_extensions.routers import ExtendedDefaultRouter

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
    ProfileViewSet,
    PublisherViewSet,
)

__all__ = ('urlpatterns',)


router = ExtendedDefaultRouter()
books = router.register(r'books',
                        BookViewSet,
                        base_name='book')
publishers = router.register(r'publishers',
                             PublisherViewSet,
                             base_name='publisher')
profiles = router.register(r'profiles',
                           ProfileViewSet,
                           base_name='profile')
authors = router.register(r'authors',
                          AuthorViewSet,
                          base_name='author')

proxy_authors = router.register(r'proxy-authors',
                                AuthorProxyViewSet,
                                base_name='authorproxy')

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
