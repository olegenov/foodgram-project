from rest_framework import permissions


class FollowPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user != obj.author
