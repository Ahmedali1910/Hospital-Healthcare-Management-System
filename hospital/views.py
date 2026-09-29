from django.shortcuts import render

from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import Department, Patient, Doctor, Appointment,Medical_Consultation,surgery,Follow_UP
from .serializers import DepartmentSerializer, PatientSerializer,DoctorSerializer,AppointmentSerializer,FollowUpSerializer,SurgerySerializer,MedicalConsultationSerializer

from user.permssions import IsAdminRole , IsDoctorRole,IsPatientRole,CanViewPatientRecords,CanViewUpdateRecords

class PatientViewset(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
   

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsAdminRole]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated,(IsPatientRole | CanViewPatientRecords)]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated,(IsPatientRole | IsAdminRole)]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminRole]    
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user=self.request.user

        if user.role == 'Admin':
            return Patient.objects.all()
        elif user.role == 'Doctor':
            return Patient.objects.filter(doctor__user=user)
        elif user.role == 'Patient':
            return Patient.objects.filter(user=user)


class DoctorViewset(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department__name']
    search_fields = ['name']
    ordering_fields = [ 'department__name' , 'name']
    ordering = ['department__name', 'name']  # by default, order by department name and then by doctor name

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsAdminRole])
    def pending_doctors(self, request):
        pending_doctors = Doctor.objects.filter(status='pending')
        serializer = DoctorSerializer(pending_doctors, many=True)
        return Response(serializer.data)

    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated , IsAdminRole ]
        elif self.action in ['list','retrieve']:
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated ,(IsDoctorRole | IsAdminRole)]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminRole]
        return [permission() for permission in permission_classes]  

    def get_queryset(self):

        if self.action == 'list':
            return Doctor.objects.filter(status='approved')
        return Doctor.objects.all()

class AppointmentViewset(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.patient)  # user don't write patient_id in request body, it will be automatically set to the logged-in user
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated,(IsPatientRole | IsAdminRole)]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, CanViewUpdateRecords]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated,CanViewUpdateRecords]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminRole]
        return [permission() for permission in permission_classes]
  
    def get_queryset(self):
            user=self.request.user
    
            if user.role == 'ADMIN':
                return Appointment.objects.all()
            elif user.role == 'Doctor':
                return Appointment.objects.filter(doctor__user=user)
            elif user.role == 'Patient':
                return Appointment.objects.filter(patient__user=user)



class MedicalConsultationViewset(viewsets.ModelViewSet):
    serializer_class = MedicalConsultationSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated,(IsDoctorRole | IsAdminRole)]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, CanViewUpdateRecords]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated,CanViewUpdateRecords]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminRole]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
            user=self.request.user
    
            if user.role == 'ADMIN':
                return Medical_Consultation.objects.all()
            elif user.role == 'Doctor':
                return Medical_Consultation.objects.filter(appointment__doctor__user=user)
            elif user.role == 'Patient':
                return Medical_Consultation.objects.filter(appointment__patient__user=user)            


class SurgeryViewset(viewsets.ModelViewSet):
    serializer_class = SurgerySerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated,(IsDoctorRole |IsAdminRole)]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, CanViewUpdateRecords]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, CanViewUpdateRecords]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminRole]
        return [permission() for permission in permission_classes]    

    def get_queryset(self):     
        user=self.request.user
    
        if user.role == 'ADMIN':
            return surgery.objects.all()
        elif user.role == 'Doctor':
            return surgery.objects.filter(medical_consultation__appointment__doctor__user=user)
        elif user.role == 'Patient':
            return surgery.objects.filter(medical_consultation__appointment__patient__user=user)

class FollowUpViewset(viewsets.ModelViewSet): 
    serializer_class = FollowUpSerializer
        
    def get_permissions(self): 
        
        if self.action == 'create':
            permission_classes = [IsAuthenticated,(IsDoctorRole | IsAdminRole)]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, CanViewUpdateRecords]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, CanViewUpdateRecords]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminRole]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user=self.request.user
    
        if user.role == 'ADMIN':
            return Follow_UP.objects.all()
        elif user.role == 'Doctor':
            return Follow_UP.objects.filter(medical_consultation__appointment__doctor__user=user)
        elif user.role == 'Patient':
            return Follow_UP.objects.filter(medical_consultation__appointment__patient__user=user)        


class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsAdminRole]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated ,(IsAdminRole | IsDoctorRole)]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsAdminRole]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminRole]
        return [permission() for permission in permission_classes]
        