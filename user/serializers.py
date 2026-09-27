from rest_framework import serializers
from .models import User
from hospital.models import Doctor, Patient



class PatientSerializer(serializers.ModelSerializer):

    name = serializers.CharField()
    age = serializers.IntegerField()
    phone = serializers.CharField()
    
    class Meta:
        model = User
        fields = ['username', 'email','name', 'age', 'phone','password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = ['role'] 

        def create(self, validated_data):
            name=validated_data.pop('name')
            age=validated_data.pop('age')
            phone=validated_data.pop('phone')

            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                role='Patient',
              )

            Patient.objects.create(
                user=user, name=name, age=age, phone=phone
            )
            return user


class DoctorSerializer(serializers.ModelSerializer):
   
    name= serializers.CharField()
    phone=serializers.CharField()   
   
    class Meta:
        model = User
        fields = ['username', 'name', 'phone', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = ['role'] 

        def create(self, validated_data):
            name=validated_data.pop('name')
            phone=validated_data.pop('phone')
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                role='Doctor',
              )
            Doctor.objects.create(
                user=user, name=name, phone=phone
            )
            return user        