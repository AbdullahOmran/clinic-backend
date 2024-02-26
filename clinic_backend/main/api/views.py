# from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
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
    ClinicSerializer,TreatmentSerializer
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


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def create_patient(request):
    serializer = PatientSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH','DELETE','PUT'])
# @permission_classes([IsAuthenticated])
def patient_details(request, pk):
    patient =  None
    try:
        patient = Patient.objects.get(id=pk)
        doctors = Doctor.objects.filter(user = request.user)
        secretaries = Secretary.objects.filter(user = request.user)
        if doctors.count() > 0:
            doctor = doctors[0]
            appointments = Appointment.objects.filter(patient=patient, doctor = doctor)
            if appointments.count() == 0:
                return Response(status=status.HTTP_403_FORBIDDEN)
    
        if secretaries.count()>0:
            secretary = secretaries[0]
            appointments = Appointment.objects.filter(patient=patient, secretary = secretary)
            if appointments.count() == 0:
                return Response(status=status.HTTP_403_FORBIDDEN)

    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PatientSerializer(patient, many = False)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = PatientSerializer(patient,data = request.data, many = False, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = PatientSerializer(patient,data = request.data, many = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
#@permission_classes([IsAuthenticated])
def create_or_appointment_list(request):
    if request.method == 'POST':
        serializer = AppointmentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        doctors = Doctor.objects.filter(user = request.user)
        secretaries = Secretary.objects.filter(user = request.user)
        if doctors.count() > 0:
            doctor = doctors[0]
            appointments = Appointment.objects.filter( doctor = doctor)
            serializer = AppointmentSerializer(appointments, many = True)
            return Response(serializer.data)
            
        if secretaries.count()>0:
            secretary = secretaries[0]
            appointments = Appointment.objects.filter(secretary = secretary)
            serializer = AppointmentSerializer(appointments, many = True)
            return Response(serializer.data)
            


@api_view(['GET', 'PATCH','DELETE','PUT'])
# @permission_classes([IsAuthenticated])
def appointment_details(request, pk):
    appointment =  None
    try:
        appointment = Appointment.objects.get(id=pk)
       

    except Appointment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = AppointmentSerializer(appointment, many = False)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = AppointmentSerializer(appointment,data = request.data, many = False, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = AppointmentSerializer(appointment,data = request.data, many = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def clinic_details(request, pk):
    clinic = Clinic.objects.get(id=pk)
    serializer = ClinicSerializer(clinic, many = False)
    return Response(serializer.data)


@api_view(['GET', 'PATCH','DELETE','PUT'])
# @permission_classes([IsAuthenticated])
def treatment_details(request, pk):
    treatment =  None
    try:
        treatment = Treatment.objects.get(id=pk)
        
    except Treatment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TreatmentSerializer(treatment, many = False)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = TreatmentSerializer(treatment,data = request.data, many = False, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        treatment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = TreatmentSerializer(treatment,data = request.data, many = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
#@permission_classes([IsAuthenticated])
def create_or_treatment_list(request):
    if request.method == 'POST':
        serializer = Treatment(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        doctors = Doctor.objects.filter(user = request.user)
        if doctors.count() > 0:
            doctor = doctors[0]
            treatments = Treatment.objects.filter( doctor = doctor)
            serializer = TreatmentSerializer(treatments, many = True)
            return Response(serializer.data)
            
        
            