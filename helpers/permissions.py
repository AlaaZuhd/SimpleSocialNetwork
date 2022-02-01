import rest_framework
from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class IsToUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.to_user.id == request.user.id


class IsPostOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner.account.user.id == request.user.id


class IsAuthenticated(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if(request.method == 'POST'):
            return True;
        else:
            print("is authenticated: " + rest_framework.permissions.IsAuthenticated)
            return rest_framework.permissions.IsAuthenticated