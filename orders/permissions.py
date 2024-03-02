from rest_framework import permissions


class IsOrderUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:

            # Check permission for read only request
            return True
        else:
            # Check permission for write request
            return obj.order_user == request.user or request.user.is_staff
