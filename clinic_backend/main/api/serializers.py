from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models import (
    Doctor, Secretary, Patient, Appointment,
     MedicationsStore, Medication, Treatment, 
     WorkingSchedule, Prescription, Encounter, 
     SymptomDiagnosisPair, Clinic, Settings,
)
from django.db.models import Q,QuerySet



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['user_first_name'] = user.first_name
        # get the clinic corresponding to that user
        
        doctors = Doctor.objects.filter(user__id = user.id)
        if doctors.count()==0:
            secretaries = Secretary.objects.filter(user__id = user.id)

        if doctors.count()>0:
            token['doctor_id'] = doctors[0].id
            token['clinic_name'] = doctors[0].clinic.name if doctors[0].clinic is not None else 'No Clinic'
        elif secretaries.count()>0:
            token['secretary_id'] = secretaries[0].id
            token['clinic_name'] = secretaries[0].clinic.name if secretaries[0].clinic is not None else 'No Clinic'
        
        # ...
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email']

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
class SecretarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Secretary
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

