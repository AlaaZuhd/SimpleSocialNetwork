import rest_framework
from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class IsToUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print("to")
        print(obj.to_user.account.user.id)
        print( request.user.id)
        return obj.to_user.account.user.id == request.user.id


class IsFromUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print("from")
        print(obj.from_user.account.user.id)
        print(request.user.id)
        return obj.from_user.account.user.id == request.user.id


class IsPostOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner.account.user.id == request.user.id


class IsLikeOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner.account.user.id == request.user.id


class IsStoryOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner.account.user.id == request.user.id

class IsCommentOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner.account.user.id == request.user.id


class IsProfileOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.account.user.id == request.user.id


class IsAuthenticated(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return rest_framework.permissions.IsAuthenticated