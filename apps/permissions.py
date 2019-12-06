from rest_framework.permissions import BasePermission


class IsStaffUser(BasePermission):
    """Class that implements is staff user permission"""

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False
