from rest_framework.permissions import BasePermission

from authapp.models import Customer


class AllowedByGroup(BasePermission):

    def has_object_permission(self, request, view, obj):
        user: Customer = request.user
        if user.is_staff and obj.group.group_name in user.groups.all().values_list('group_name', flat=True):
            return True
        if obj.customer == user:
            return True
        return False
