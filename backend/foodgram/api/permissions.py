from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Permission class that allows read-only access for unauthenticated users.

    Full access for authenticated users, including admin users.

    For safe methods (GET, HEAD, OPTIONS), all users are allowed.
    For other methods, only authenticated users with admin privileges
    or the author of the object are allowed.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_staff
        )
