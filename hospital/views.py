from django.http import request
from django.shortcuts import render

from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import Department, Patient, Doctor, Appointment,Medical_Consultation,surgery,Follow_UP,Status
from .serializers import DepartmentSerializer, DoctorAdminSerializer, PatientSerializer,DoctorSerializer,AppointmentSerializer,FollowUpSerializer,SurgerySerializer,MedicalConsultationSerializer

from user.permssions import IsAdminRole, IsDoctor , IsDoctorRole,IsPatientRole,CanViewPatientRecords,CanViewUpdateRecords

class PatientViewset(viewsets.ModelViewSet):
    serializer_class = PatientSerializer

    @action(detail=False,methods=['patch','put'],permission_classes=[IsAuthenticated,(IsPatientRole | IsAdminRole)])
    def me(self, request):
       patient = request.user.patient
       if request.method == 'PATCH':
           serializer = PatientSerializer(
               patient,
               data=request.data,
               partial=True
           )
           serializer.is_valid(raise_exception=True)
           serializer.save()
           return Response(serializer.data)
       elif request.method == 'PUT':
           serializer = PatientSerializer(
               patient,
               data=request.data
           )
           serializer.is_valid(raise_exception=True)
           serializer.save()
           return Response(serializer.data)         
       

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsAdminRole]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated,(IsPatientRole | CanViewPatientRecords)]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated,(IsPatientRole | IsAdminRole)]
        elif self.action == 'me':
            permission_classes = [IsAuthenticated, (IsPatientRole | IsAdminRole)]    
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

    @action(detail=False,methods=['get', 'patch','put'],permission_classes=[IsAuthenticated, IsDoctor])
    def me(self, request):
        doctor = request.user.doctor

        if request.method == 'GET':
             serializer = DoctorSerializer(doctor)
             return Response(serializer.data)
        elif request.method in ['PATCH']:
            serializer = DoctorSerializer(doctor,data=request.data,partial=True)
            serializer.is_valid(raise_exception=True) 
            serializer.save()
            return Response(serializer.data)
        elif request.method in ['PUT']:
            serializer = DoctorSerializer(doctor,data=request.data)
            serializer.is_valid(raise_exception=True) 
            serializer.save()
            return Response(serializer.data)

    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated , IsAdminRole ]
        elif self.action in ['list','retrieve']:
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated ,(IsDoctor | IsAdminRole)]
        elif self.action == 'me':
            permission_classes = [IsAuthenticated, IsDoctor]
        elif self.action == 'pending_doctors':
            permission_classes = [IsAuthenticated, IsAdminRole]    
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminRole]
        return [permission() for permission in permission_classes]  

    def get_queryset(self):

        if self.action == 'list':
            return Doctor.objects.filter(status='approved')
        return Doctor.objects.all()


class DoctorAdminViewset(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


    

class AppointmentViewset(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user.patient)  # user don't write patient_id in request body, it will be automatically set to the logged-in user

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):

       appointment = self.get_object()

       if appointment.status == Status.COMPLETED:
         return Response(
           {"detail": "Completed appointment cannot be cancelled."},
            status=status.HTTP_400_BAD_REQUEST
        )
       
       if request.user.role == 'Patient':

          if appointment.patient.user != request.user:
              return Response(
                  {"detail": "You can only cancel your own appointments."},
                  status=status.HTTP_403_FORBIDDEN
              )
 
       elif request.user.role == 'Doctor':

          if appointment.doctor.user != request.user:
              return Response(
                  {"detail": "You can only cancel your own appointments."},
                  status=status.HTTP_403_FORBIDDEN
                )

       elif request.user.role != 'Admin':

           return Response(
               {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN
            )

       appointment.status = Status.CANCELLED
       appointment.save()

       return Response(
            AppointmentSerializer(appointment).data
        )
    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):

      appointment = self.get_object()

      if appointment.status == Status.CANCELLED:
          return Response(
             {"detail": "Cancelled appointment cannot be completed."},
              status=status.HTTP_400_BAD_REQUEST
            )

      if request.user.role == 'Doctor':

           if appointment.doctor.user != request.user:
             return Response(
                   {"detail": "You can only complete your own appointments."},
                  status=status.HTTP_403_FORBIDDEN
              )

      elif request.user.role != 'Admin':

           return Response(
                {"detail": "Only doctor or admin can complete an appointment."},
                  status=status.HTTP_403_FORBIDDEN
               )

      appointment.status = Status.COMPLETED
      appointment.save()

      return Response(
         AppointmentSerializer(appointment).data
        )
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated,(IsPatientRole | IsAdminRole)]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, CanViewUpdateRecords]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated,IsPatientRole | IsAdminRole]
        elif self.action in ['complete']:
            permission_classes = [
                IsAuthenticated, (IsDoctorRole | IsAdminRole)
            ]
        elif self.action in ['cancel']:
            permission_classes = [
                IsAuthenticated, (IsPatientRole | IsDoctorRole | IsAdminRole)
            ]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminRole]
        return [permission() for permission in permission_classes]
  
    def get_queryset(self):
            user=self.request.user
    
            if user.role == 'Admin':
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
            permission_classes = [IsAuthenticated,IsDoctorRole | IsAdminRole]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminRole]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
            user=self.request.user
    
            if user.role == 'Admin':
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
            permission_classes = [IsAuthenticated, IsDoctorRole|IsAdminRole]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminRole]
        return [permission() for permission in permission_classes]    

    def get_queryset(self):     
        user=self.request.user
    
        if user.role == 'Admin':
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
            permission_classes = [IsAuthenticated, IsDoctorRole|IsAdminRole]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminRole]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user=self.request.user
    
        if user.role == 'Admin':
            return Follow_UP.objects.all()
        elif user.role == 'Doctor':
            return Follow_UP.objects.filter(medical_consultation__appointment__doctor__user=user)
        elif user.role == 'Patient':
            return Follow_UP.objects.filter(medical_consultation__appointment__patient__user=user)        


class DepartmentViewset(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]

        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminRole]

        return [permission() for permission in permission_classes]
        