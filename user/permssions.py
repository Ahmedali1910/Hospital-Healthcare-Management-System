from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    message = "Access denied. Admin role required."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role =='ADMIN')

class IsDoctorRole (BasePermission):
    message = "Access denied. Doctor role required."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role =='Doctor' and request.user.doctor.status == 'approved')
    def has_object_permission(self, request, view, obj):
        return  obj.user == request.user

class IsPatientRole (BasePermission):
    message = "Access denied. Patient role required."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role =='Patient')

    def has_object_permission(self, request, view, obj):
        return  obj.user == request.user

class CanViewPatientRecords(BasePermission):
    message = "Access denied. You do not have permission to view patient records."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role == 'ADMIN' or request.user.role == 'Doctor' and request.user.doctor.status == 'approved'))

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
        
        elif request.user.role == 'Doctor':
            return obj.doctor_id.user == request.user

        return False    

class CanViewUpdateRecords(BasePermission):
    message = "Access denied. You do not have permission to view appointment records."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role == 'ADMIN' or (request.user.role == 'Doctor' and request.user.doctor.status == 'approved') or request.user.role == 'Patient'))

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
        
        elif request.user.role == 'Doctor':
            return obj.doctor_id.user == request.user

        elif request.user.role == 'Patient':
            return obj.patient_id.user == request.user

        return False    
