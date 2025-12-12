from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """ Проверяет, является ли пользователем автором записи"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
