from rest_framework import permissions

class UserEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id:
            return True
        return False

class CheckUserSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'seller':
            return True
        return False


class CheckUserBuyer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'buyer':
            return True
        return False


class CheckCarEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.seller == request.user:
            return True
        return False


class CheckAuctionEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.car.seller == request.user:
            return True
        return False