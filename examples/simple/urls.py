"""
Urls.
"""

from django.urls import include, re_path as url, path
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.generic import TemplateView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from books import urls as books_urls

__all__ = ("urlpatterns",)

admin.autodiscover()

urlpatterns = []
urlpatterns_args = []

# Admin URLs
urlpatterns_args += [
    url(r"^admin/", admin.site.urls),
]

urlpatterns_args = [
    # Books URLs
    url(r"^books/", include(books_urls)),
    # Home page
    url(r"^$", TemplateView.as_view(template_name="home.html")),

    # Schema
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns += urlpatterns_args[:]

# Serving media and static in debug/developer mode.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

    if settings.DEBUG_TOOLBAR is True:
        import debug_toolbar

        urlpatterns = [
            url(r"^__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns
