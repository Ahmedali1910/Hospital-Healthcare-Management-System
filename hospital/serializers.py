from rest_framework import serializers
from .models import Department, Patient, Doctor, Appointment,Medical_Consultation,surgery,Follow_UP

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'        

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
    def validate(self, data):
        doctor = data.get('doctor_id')
        date = data.get('date')
        time = data.get('time')

        existing_appointments = Appointment.objects.filter(doctor_id=doctor, date=date, time=time).exclude(status='cancelled').exists()
        if existing_appointments:
            raise serializers.ValidationError("The doctor is already booked for this date and time.")
        return data

class MedicalConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medical_Consultation
        fields = '__all__'  

class SurgerySerializer(serializers.ModelSerializer):
    class Meta:
        model = surgery
        fields = '__all__'                   

class FollowUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow_UP
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'       

