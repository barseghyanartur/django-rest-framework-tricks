from django_filters import filters
from django_filters.rest_framework import FilterSet

from .models import Book


class CustomStateFilter(filters.CharFilter):
    """Custom state filter."""

    def __init__(self, *args, **kwargs):
        kwargs.update({'field_name': 'status'})
        super(CustomStateFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value == 'non-published':
            qs = qs.filter(
                state__in=[
                    'not_published',
                    'in_progress',
                    'cancelled',
                    'rejected',
                ]
            )
            return qs
        elif value == 'published':
            qs = qs.filter(state='published')
            return qs
        else:
            return super(CustomStateFilter, self).filter(qs, value)


class CustomStatusFilter(FilterSet):
    """Custom state filter set."""

    status = CustomStateFilter()

    class Meta(object):
        """Options."""

        model = Book
        fields = ['id', 'status']
