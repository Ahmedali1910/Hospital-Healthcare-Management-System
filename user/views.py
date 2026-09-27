from django.shortcuts import render

# Create your views here.

from rest_framework.generics import CreateAPIView
from .serializers import PatientSerializer, DoctorSerializer

# Create your views here.
class PatientCreateView(CreateAPIView):
    serializer_class = PatientSerializer

class DoctorCreateView(CreateAPIView):
    serializer_class = DoctorSerializer