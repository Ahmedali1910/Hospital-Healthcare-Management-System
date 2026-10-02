from rest_framework import serializers
from .models import User
from hospital.models import Doctor, Patient



class PatientRegistrationSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.EmailField()

    name = serializers.CharField()
    age = serializers.IntegerField()
    phone = serializers.CharField()

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError("Passwords don't match")

        return data

    def create(self, validated_data):
        name = validated_data.pop('name')
        age = validated_data.pop('age')
        phone = validated_data.pop('phone')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='Patient',
        )

        patient = Patient.objects.create(
            user=user,
            name=name,
            age=age,
            phone=phone
        )

        return patient

        

class DoctorRegistrationSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.EmailField()

    name = serializers.CharField()
    phone = serializers.CharField()

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError("Passwords don't match")

        return data

    def create(self, validated_data):
        name = validated_data.pop('name')
        phone = validated_data.pop('phone')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='Doctor',
        )

        doctor = Doctor.objects.create(
            user=user,
            name=name,
            phone=phone
        )

        return doctor