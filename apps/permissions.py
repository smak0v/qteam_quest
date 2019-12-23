from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffUser(BasePermission):
    """Class that implements is staff user permission"""

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class IsStaffUserOrReadOnly(BasePermission):
    """Class that implements is staff or read only permission"""

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )
