from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from hospital.serializers import PatientSerializer, DoctorSerializer
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from .serializers import PatientRegistrationSerializer, DoctorRegistrationSerializer
# Create your views here.
class PatientCreateView(CreateAPIView):
    serializer_class = PatientRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = serializer.save()

        return Response(
            PatientSerializer(patient).data,
            status=status.HTTP_201_CREATED
        )

class DoctorCreateView(CreateAPIView):
    serializer_class = DoctorRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        doctor = serializer.save()

        return Response(
            DoctorSerializer(doctor).data,
            status=status.HTTP_201_CREATED
        )