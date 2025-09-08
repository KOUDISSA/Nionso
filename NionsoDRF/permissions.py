from rest_framework import permissions

class IsManager(permissions.BasePermission):
    """class to personalize permissions for manager only"""
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.groups.filter(name='Manager').exists()
        return False