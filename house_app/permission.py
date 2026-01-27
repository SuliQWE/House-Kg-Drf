from rest_framework.permissions import BasePermission


class CreatePropertyPermission(BasePermission):
    def has_object_permission (self, request, view):
        if request.user.role == 'seller':
            return True
        return False


class CreateReviewPermission(BasePermission):
    def has_object_permission (self, request, view):
        if request.user.role == 'buyer':
            return True
        return False