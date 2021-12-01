"""
Ordering filter.
"""

from rest_framework.filters import OrderingFilter as DjangoOrderingFilter

__title__ = "rest_framework_tricks.filters.ordering"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = ("OrderingFilter",)


class OrderingFilter(DjangoOrderingFilter):
    """Ordering filter improved.

    Example:

    >>> from rest_framework_tricks.filters import OrderingFilter
    >>>
    >>> class BooksViewSet(mixins.RetrieveModelMixin,
    >>>                    mixins.ListModelMixin,
    >>>                    viewsets.GenericViewSet):
    >>>
    >>>     serializer_class = BookSerializer
    >>>     filter_backends = (
    >>>         OrderingFilter,
    >>>     )
    >>>     ordering_fields = {
    >>>         'email': 'user__email',
    >>>         'full_name': 'user__first_name',
    >>>         'last_login': 'user__last_login',
    >>>         'is_active': 'user__is_active',
    >>>     }

    Then it can be used in a view set as follows:

        GET /books/api/proxy-books/?ordering=email
    """

    def get_valid_fields(self, queryset, view, context={}):
        """Done.

        :param queryset:
        :param view:
        :param context:
        :return:
        """
        valid_fields = getattr(view, "ordering_fields", self.ordering_fields)

        if isinstance(valid_fields, dict):
            return valid_fields.items()
        else:
            return super(OrderingFilter, self).get_valid_fields(queryset, view, context)

    def get_ordering(self, request, queryset, view):
        """Get ordering.

        Important: list returned in this method is used directly
        in the filter_queryset method like:

        >>> queryset.order_by(*ordering)

        Ordering is set by a comma delimited ?ordering=... query parameter.

        The `ordering` query parameter can be overridden by setting
        the `ordering_param` value on the OrderingFilter or by
        specifying an `ORDERING_PARAM` value in the API settings.
        """
        valid_fields = getattr(view, "ordering_fields", self.ordering_fields)

        # If valid_fields is a dictionary, treat it differently
        if isinstance(valid_fields, dict):
            params = request.query_params.get(self.ordering_param)

            if params:
                fields = [param.strip() for param in params.split(",")]
                _ordering = self.remove_invalid_fields(queryset, fields, view, request)

                ordering = []
                for item in _ordering:
                    if "-" in item:
                        value = valid_fields.get(item[1:])
                        if isinstance(value, (tuple, list)):
                            value = ["-{}".format(__v) for __v in value]
                            ordering += value
                        else:
                            ordering.append("-{}".format(value))
                    else:
                        value = valid_fields.get(item)
                        if isinstance(value, (tuple, list)):
                            ordering += value
                        else:
                            ordering.append(value)
                if ordering:
                    return ordering

            # No ordering was included, or all the ordering fields were invalid
            return self.get_default_ordering(view)

        # In all other cases, use default behaviour
        else:
            return super(OrderingFilter, self).get_ordering(request, queryset, view)
