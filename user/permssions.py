from rest_framework.permissions import BasePermission
from hospital.models import Follow_UP,surgery,Medical_Consultation,Appointment
class IsAdminRole(BasePermission):
    message = "Access denied. Admin role required."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role =='ADMIN')

class IsDoctorRole (BasePermission):
    message = "Access denied. Doctor role required."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role =='Doctor' and request.user.doctor.status == 'approved')
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
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
            return obj.doctor.user == request.user

        return False    

class CanViewUpdateRecords(BasePermission):
    message = "Access denied. You do not have permission to view appointment records."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role == 'ADMIN' or (request.user.role == 'Doctor' and request.user.doctor.status == 'approved') or request.user.role == 'Patient'))

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True

        if isinstance (obj,Appointment):
            if request.user.role=='Patient':
               return obj.patient.user==request.user
            if request.user.role == 'Doctor':
                return obj.doctor.user == request.user
        elif isinstance(obj, Medical_Consultation):
            if request.user.role == 'Doctor':
                return obj.appointment.doctor.user == request.user

            if request.user.role == 'Patient':
                return obj.appointment.patient.user == request.user

        elif isinstance(obj, Follow_UP):
            if request.user.role == 'Doctor':
                return obj.medical_consultation.appointment.doctor.user == request.user

            if request.user.role == 'Patient':
                return obj.medical_consultation.appointment.patient.user == request.user

        elif isinstance(obj, surgery):
            if request.user.role == 'Doctor':
                return obj.medical_consultation.appointment.doctor.user == request.user

            if request.user.role == 'Patient':
                return obj.medical_consultation.appointment.patient.user == request.user

        return False    
