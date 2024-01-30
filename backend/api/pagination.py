from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)

from .constants import (RECIPE_PAGINATION_PAGE_SIZE,
                        USER_PAGINATION_DEFAULT_LIMIT,
                        USER_PAGINATION_PAGE_SIZE)


class RecipePagination(PageNumberPagination):
    """Recipe list pagination."""

    page_size = RECIPE_PAGINATION_PAGE_SIZE
    page_size_query_param = 'limit'


class UserPagination(PageNumberPagination, LimitOffsetPagination):
    """User list pagination."""

    page_size = USER_PAGINATION_PAGE_SIZE
    default_limit = USER_PAGINATION_DEFAULT_LIMIT
    page_size_query_param = 'limit'
