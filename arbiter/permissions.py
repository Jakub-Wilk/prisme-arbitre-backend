from rest_framework import permissions


class IsOwnerOrStaffElseReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.user

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        print(request.user.is_staff)
        print(obj.user == request.user)
        if obj.user:
            return obj.user == request.user
        return request.user.is_staff
