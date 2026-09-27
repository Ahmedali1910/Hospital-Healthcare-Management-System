from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import PatientCreateView, DoctorCreateView

urlpatterns = [
    path('register/patients/', PatientCreateView.as_view(), name='patient_create'),
    path('register/doctors/', DoctorCreateView.as_view(), name='doctor_create'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]