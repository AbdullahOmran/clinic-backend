# from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken

from django.http import JsonResponse
from django.contrib.auth.models import User
from ..models import (
    Doctor, Secretary, Patient, Appointment,
     MedicationsStore, Medication, Treatment, 
     WorkingSchedule, Prescription, Encounter, 
     SymptomDiagnosisPair, Clinic, Settings,
)

from .serializers import (
    UserSerializer, MyTokenObtainPairSerializer,DoctorSerializer,
    SecretarySerializer, PatientSerializer,AppointmentSerializer,
    ClinicSerializer,
)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/token/refresh/',
    ]
    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many = False)
    access_token = request.headers.get('Authorization')[7:]
    decoded_token = AccessToken(access_token).payload
    print(decoded_token)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def doctor_details(request, pk):
    doctor = Doctor.objects.get(id=pk)
    serializer = DoctorSerializer(doctor, many = False)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def secretary_details(request, pk):
    secretary = Secretary.objects.get(id=pk)
    serializer = SecretarySerializer(secretary, many = False)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def patient_details(request, pk):
    patient = Patient.objects.get(id=pk)
    serializer = PatientSerializer(patient, many = False)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def appointment_details(request, pk):
    appointment = Appointment.objects.get(id=pk)
    serializer = AppointmentSerializer(appointment, many = False)
    return Response(serializer.data)

# @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# def clinic_details(request, pk):
#     clinic = Clinic.objects.get(id=pk)
#     serializer = ClinicSerializer(clinic, many = False)
#     return Response(serializer.data)
