from django.urls import path,include
from .views import DoctorAdminViewset, PatientViewset,DepartmentViewset,DoctorViewset,AppointmentViewset,FollowUpViewset,SurgeryViewset,MedicalConsultationViewset
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'patients',PatientViewset,basename='patients')
router.register(r'doctors',DoctorViewset,basename='doctors')
router.register(r'appointments',AppointmentViewset,basename='appointments')
router.register(r'follow-ups',FollowUpViewset,basename='follow-ups')
router.register(r'surgeries',SurgeryViewset,basename='surgeries')
router.register(r'medical-consultations',MedicalConsultationViewset,basename='medical-consultations')
router.register(r'departments',DepartmentViewset,basename='departments')
router.register(r'doctors-admin',DoctorAdminViewset,basename='doctors-admin') 
urlpatterns = [
   path('',include(router.urls)),
]