from django.db import models

# Create your models here.
class Status(models.TextChoices):
    SCHEDULED = 'Scheduled'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'

class Department (models.Model):
     name=models.CharField(max_length=50)


class Doctor (models.Model):
     name=models.CharField(max_length=50)
     department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
     phone=models.CharField(max_length=20)
     email=models.EmailField()

class Patient (models.Model):
    name=models.CharField(max_length=50)
    age=models.IntegerField()
    phone=models.CharField(max_length=20)
    doctor_id=models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True)

class Appointment(models.Model):
    patient_id=models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField()    
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.SCHEDULED)

class Medical_Consultation(models.Model):
     type_Of_Medical_Consultation=models.CharField(100)
     doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
     patient_id=models.ForeignKey(Patient,on_delete=models.CASCADE)
     symptoms=models.TextField()
     status=models.CharField(max_length=20,choices=Status.choices,default=Status.SCHEDULED)
     diagnosis=models.TextField()
     treatment=models.TextField()
     notes=models.TextField()
     appointment_id=models.OneToOneField(Appointment,on_delete=models.CASCADE)

class Follow_UP(models.Model):
     medical_consultation_id=models.ForeignKey(Medical_Consultation,on_delete=models.CASCADE)
     patient_id=models.ForeignKey(Patient,on_delete=models.CASCADE)
     doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
     date=models.DateTimeField()
     notes=models.TextField()
     status=models.CharField(max_length=20,choices=Status.choices,default=Status.SCHEDULED)

class surgery(models.Model):
     name=models.CharField(100)
     doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
     patient_id=models.ForeignKey(Patient,on_delete=models.CASCADE)
     date=models.DateTimeField()
     status=models.CharField(max_length=20,choices=Status.choices,default=Status.SCHEDULED)
     medical_consultation_id=models.ForeignKey(Medical_Consultation,on_delete=models.CASCADE)

