from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "STUDENT" 
    

class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "INSTRUCTOR"

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "ADMIN"