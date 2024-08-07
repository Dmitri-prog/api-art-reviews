from rest_framework import permissions

from users.models import ADMIN, USER


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.role == ADMIN)
        )


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and (request.user.is_superuser
                 or request.user.role == ADMIN)
        )


class IsAuthorOrAdmin(permissions.BasePermission):
    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, object):
        return (request.method in permissions.SAFE_METHODS
                or object.author == request.user
                or request.user.role != USER)
