from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly


class IsAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Permission class that allows read-only access for unauthenticated users.
    For safe methods (GET, HEAD, OPTIONS), all users are allowed.
    For other methods, only authenticated users with admin privileges
    or the author of the object are allowed.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_staff
                or request.user.is_superuser
                or obj.author == request.user
                )
