# from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .utils import get_payload

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
def user_details(request):
    user = request.user
    serializer = UserSerializer(user, many = False)
    return Response(serializer.data)

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def doctor_details(request):
    doctor = None
    try:
        doctor = Doctor.objects.get(user = request.user)
    except Doctor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DoctorSerializer(doctor, many = False)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def secretary_details(request):
    secretary = None
    try:
        secretary = Secretary.objects.get(user = request.user)
    except Secretary.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SecretarySerializer(secretary, many = False)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = SecretarySerializer(secretary, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)





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
