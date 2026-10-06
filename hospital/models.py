from django.db import models
from user.models import User

# Create your models here.
class Status(models.TextChoices):
    SCHEDULED = 'Scheduled'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'

class Department (models.Model):
     name=models.CharField(max_length=50)
     def __str__(self):
         return self.name


class Doctor (models.Model):
     STATUS_CHOICES = [
         ('pending', 'Pending'),
         ('approved', 'Approved'),
         ('rejected', 'Rejected'),
     ]
     user=models.OneToOneField(User,on_delete=models.CASCADE)
     name=models.CharField(max_length=50)
     department=models.ForeignKey(Department,on_delete=models.CASCADE,null=True) #frontend will send department_id in request body because the doctor choose the department after creating the doctor.
     phone=models.CharField(max_length=20)
     status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')

     def __str__(self):
         return self.name

class Patient (models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    age=models.IntegerField()
    phone=models.CharField(max_length=20)
    doctor=models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True) #frontend will send doctor_id in request body because the patient choose the doctor after creating the patient.
    def __str__(self):
        return self.name 
    
class Appointment(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE) # patient_id will be automatically set to the logged-in user when creating an appointment, so the frontend don't need to send it in request body
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE) # frontend will send doctor_id in request body,he know because the patient choose the doctor before creating the appointment, and it will be used to create the appointment
    date=models.DateField()
    time=models.TimeField()    
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.SCHEDULED)
    def __str__(self):
        return f"Appointment for {self.patient.name} with dr-{self.doctor.name} on {self.date} at {self.time}"

class Medical_Consultation(models.Model):
     type_Of_Medical_Consultation=models.CharField(max_length=100)
     status=models.CharField(max_length=20,choices=Status.choices,default=Status.SCHEDULED)
     diagnosis=models.TextField(blank=True)
     treatment=models.TextField(blank=True)
     notes=models.TextField(blank=True)
     appointment=models.OneToOneField(Appointment,on_delete=models.CASCADE) #frontend will send appointment_id in request body, because the medical consultation is created after the appointment is created, and it will be used to create the medical consultation, this include patient_id and doctor_id because the appointment include patient_id and doctor_id
     def __str__(self):
         return f"Medical Consultation for {self.appointment.patient.name} with dr-{self.appointment.doctor.name} on {self.appointment.date} at {self.appointment.time}"
class Follow_UP(models.Model):
     medical_consultation=models.ForeignKey(Medical_Consultation,on_delete=models.CASCADE) #frontend will send medical_consultation_id in request body, because the follow up is created after the medical consultation is created, and it will be used to create the follow up, this include patient_id and doctor_id  because medical include appointment where appointment include patient_id and doctor_id
     date=models.DateTimeField()
     notes=models.TextField(blank=True)
     status=models.CharField(max_length=20,choices=Status.choices,default=Status.SCHEDULED)
     def __str__(self):
         return f"Follow Up for {self.medical_consultation.appointment.patient.name} with dr-{self.medical_consultation.appointment.doctor.name} on {self.date}"
class surgery(models.Model):
     name=models.CharField(max_length=100)
     medical_consultation=models.ForeignKey(Medical_Consultation,on_delete=models.CASCADE) #frontend will send medical_consultation_id in request body, because the surgery is created after the medical consultation is created, and it will be used to create the surgery,this include patient_id and doctor_id  because medical include appointment where appointment include patient_id and doctor_id
     date=models.DateTimeField()
     notes=models.TextField(blank=True)
     status=models.CharField(max_length=20,choices=Status.choices,default=Status.SCHEDULED)
     def __str__(self):
         return f"Surgery for {self.medical_consultation.appointment.patient.name} with dr-{self.medical_consultation.appointment.doctor.name} on {self.date}"
