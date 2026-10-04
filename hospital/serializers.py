from rest_framework import serializers
from .models import Department, Patient, Doctor, Appointment,Medical_Consultation, Status,surgery,Follow_UP

class PatientSerializer(serializers.ModelSerializer):
    
     username = serializers.CharField(
        source='user.username',
        read_only=True
    )

     email = serializers.EmailField(
        source='user.email',
        read_only=True
    )
     class Meta:
        model = Patient
        fields = ['id', 'username', 'email', 'name', 'age', 'phone','doctor']

class DoctorSerializer(serializers.ModelSerializer):
     username = serializers.CharField(
        source='user.username',
        read_only=True
    )

     email = serializers.EmailField(
        source='user.email',
        read_only=True
    )
    
     class Meta:
        model = Doctor
        fields = ['id', 'username', 'email', 'name', 'department', 'phone','status']   
        read_only_fields = ['status']  # Make the status field read-only

class DoctorAdminSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    email = serializers.EmailField(
        source='user.email',
        read_only=True
    )
    
    class Meta:
        model = Doctor
        fields = ['id', 'username', 'email', 'name', 'department', 'phone','status']        

class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = [
            'id',
            'doctor',
            'date',
            'time',
            'status',
        ]

        read_only_fields = ['id', 'status']

    def validate(self, data):

        doctor = data.get(
            'doctor',
            self.instance.doctor if self.instance else None
        )

        date = data.get(
            'date',
            self.instance.date if self.instance else None
        )

        time = data.get(
            'time',
            self.instance.time if self.instance else None
        )

        if Appointment.objects.filter(
            doctor=doctor,
            date=date,
            time=time,
        ).exclude(
            id=self.instance.id if self.instance else None
        ).exclude(
            status=Status.CANCELLED
        ).exists():

            raise serializers.ValidationError(
                "The doctor is already booked for this date and time."
            )

        return data
    

class MedicalConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medical_Consultation
        fields = '__all__' 

    def validate(self, data):# I use it specifically when the `action` value is 'create' to ensure that the doctor is the same one assigned to the appointment.
      appointment = data.get(
            'appointment',
             self.instance.appointment if self.instance else None
            )
      request=self.context['request']
      if request.user.role != 'ADMIN':
           if appointment.doctor.user != request.user:
               raise serializers.ValidationError(
                  "This appointment does not belong to you."
            )
      return data 

class SurgerySerializer(serializers.ModelSerializer):
    class Meta:
        model = surgery
        fields = '__all__'  

    def validate(self, data):# I use it specifically when the `action` value is 'create' to ensure that the doctor is the same one assigned to the appointment.
        medical_consultation = data['medical_consultation']
        request = self.context['request']

        if request.user.role != 'ADMIN':
            if medical_consultation.appointment.doctor.user != request.user:
                raise serializers.ValidationError(
                    "This medical consultation does not belong to you."
                )

        return data                     

class FollowUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow_UP
        fields = '__all__'

    def validate(self,data):# I use it specifically when the `action` value is 'create' to ensure that the doctor is the same one assigned to the appointment.
        medical_consultation = data['medical_consultation']   
        request=self.context['request']
        if request.user.role != 'ADMIN':
            if medical_consultation.appointment.doctor.user != request.user:
                raise serializers.ValidationError(
                    "This medical consultation does not belong to you."
                )
        return data    


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'       

