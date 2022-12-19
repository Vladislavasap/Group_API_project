from custom_user.models import User
from rest_framework.permissions import SAFE_METHODS, BasePermission


class UserPermission(BasePermission):
    """Разрешения для действий с пользователями для пользователей"""
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, view, request, obj):
        return request.method in ('PATCH', 'GET')


class IsAdminOrReadOnly(BasePermission):
    """Разрешения для действий с названиями, жанрами и категориями"""
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == User.ADMIN
            or request.user.is_superuser
        )


class IsAdmin(BasePermission):
    """Разрешения для действий с пользователями от имени администратора"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.ADMIN
            or request.user.is_staff
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.method in ('GET', 'POST', 'PATCH', 'DELETE')