from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)


class RecipePagination(PageNumberPagination):
    """Recipe list pagination."""

    page_size = 6
    page_size_query_param = 'limit'


class UserPagination(PageNumberPagination, LimitOffsetPagination):
    """User list pagination."""

    page_size = 10
    default_limit = 10
    page_size_query_param = 'limit'
