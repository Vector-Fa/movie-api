from rest_framework.permissions import BasePermission

from apps.exceptions import ForbiddenException


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_admin:
                return True
            else:
                raise ForbiddenException('You are not an admin')




