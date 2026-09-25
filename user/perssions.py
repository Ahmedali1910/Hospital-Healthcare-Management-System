from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    message = "Access denied. Admin role required."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role =='ADMIN')

class IsDoctorRole (BasePermission):
    message = "Access denied. Doctor role required."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role =='Doctor')

class IsPatientRole (BasePermission):
    message = "Access denied. Patient role required."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role =='Patient')
    