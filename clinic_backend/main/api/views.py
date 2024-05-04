# from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from .utils import get_payload
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from ..models import (
    Doctor, Secretary, Patient, Appointment,
     MedicationsStore, Medication, Treatment, 
     WorkingSchedule, Prescription, Encounter, 
     SymptomDiagnosisPair, Clinic, Settings,ClinicUser,AppointmentSettings,
     BufferTime,
)

from .serializers import (
    UserSerializer, MyTokenObtainPairSerializer,DoctorSerializer,
    SecretarySerializer, PatientSerializer,AppointmentSerializer,
    ClinicSerializer,TreatmentSerializer,EncounterSerializer,
    MedicationSerializer,AppointmentSettingsSerializer, ClinicAvailabilitySerializer,
    BufferTimeSerializer,
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


@api_view(['POST', 'GET'])
#@permission_classes([IsAuthenticated])
def create_or_patient_list(request):
    if request.method == 'POST':
        serializer = PatientSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many = True)
        return Response(serializer.data)


@api_view(['GET', 'PATCH','DELETE','PUT'])
# @permission_classes([IsAuthenticated])
def patient_details(request, pk):
    patient =  None
    try:
        patient = Patient.objects.get(id=pk)
        # doctors = Doctor.objects.filter(user = request.user)
        # secretaries = Secretary.objects.filter(user = request.user)
        # if doctors.count() > 0:
        #     doctor = doctors[0]
        #     appointments = Appointment.objects.filter(patient=patient, doctor = doctor)
        #     if appointments.count() == 0:
        #         return Response(status=status.HTTP_403_FORBIDDEN)
    
        # if secretaries.count()>0:
        #     secretary = secretaries[0]
        #     appointments = Appointment.objects.filter(patient=patient, secretary = secretary)
        #     if appointments.count() == 0:
        #         return Response(status=status.HTTP_403_FORBIDDEN)

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
            return Response(serializer.data, status = status.HTTP_201_CREATED)
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
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        doctors = Doctor.objects.filter(user = request.user)
        if doctors.count() > 0:
            doctor = doctors[0]
            treatments = Treatment.objects.filter( doctor = doctor)
            serializer = TreatmentSerializer(treatments, many = True)
            return Response(serializer.data)
            

@api_view(['GET', 'PATCH','DELETE','PUT'])
# @permission_classes([IsAuthenticated])
def encounter_details(request, pk):
    encounter =  None
    try:
        encounter = Encounter.objects.get(id=pk)
        
    except Encounter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = EncounterSerializer(encounter, many = False)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = EncounterSerializer(treatment,data = request.data, many = False, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        encounter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = EncounterSerializer(encounter,data = request.data, many = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
#@permission_classes([IsAuthenticated])
def create_or_encounter_list(request):
    if request.method == 'POST':
        serializer = EncounterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        doctors = Doctor.objects.filter(user = request.user)
        if doctors.count() > 0:
            doctor = doctors[0]
            treatments = Treatment.objects.filter( doctor = doctor)
            encounters = Encounter.objects.filter(treatment__in = treatments) 
            serializer = EncounterSerializer(encounters, many = True)
            return Response(serializer.data)



@api_view(['GET', 'PATCH','DELETE','PUT'])
# @permission_classes([IsAuthenticated])
def medication_details(request, pk):
    medication =  None
    try:
        medication = Medication.objects.get(id=pk)
        
    except Medication.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MedicationSerializer(medication, many = False)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = MedicationSerializer(medication,data = request.data, many = False, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        medication.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = MedicationSerializer(medication,data = request.data, many = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
#@permission_classes([IsAuthenticated])
def create_or_medication_list(request):
    if request.method == 'POST':
        serializer = MedicationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        doctors = Doctor.objects.filter(user = request.user)
        if doctors.count() > 0:
            doctor = doctors[0]
            treatments = Treatment.objects.filter( doctor = doctor)
            encounters = Encounter.objects.filter(treatment__in = treatments) 
            medications = Medication.objects.filter(encounter__in = encounters)
            serializer = MedicationSerializer(medications, many = True)
            return Response(serializer.data)

class AppointmentSettingsView(APIView):
    def post(self, request):
        serializer = AppointmentSettingsSerializer(data = request.data)
        if serializer.is_valid():
            instance = serializer.save()
            clinic_user_details = ClinicUser.objects.get(user = request.user)
            clinic_user_details.clinic.appointment_settings = instance
            clinic_user_details.clinic.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self,request):
        clinic_user_details = ClinicUser.objects.get(user = request.user)
        appointment_settings_details = clinic_user_details.clinic.appointment_settings
        serializer = AppointmentSettingsSerializer(appointment_settings_details,data = request.data, many = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        clinic_user_details = ClinicUser.objects.get(user = request.user)
        appointment_settings_details = clinic_user_details.clinic.appointment_settings
        serializer = AppointmentSettingsSerializer(appointment_settings_details, many = False)
        return Response(serializer.data)

class ClinicAvailabilityView(APIView):

    def post(self, request):
        serializer = ClinicAvailabilitySerializer(data = request.data)
        if serializer.is_valid():
            instance = serializer.save()
            clinic_user_details = ClinicUser.objects.get(user = request.user)
            clinic_user_details.clinic.availability = instance
            clinic_user_details.clinic.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        clinic_user_details = ClinicUser.objects.get(user = request.user)
        availability_details = clinic_user_details.clinic.availability
        serializer = ClinicAvailabilitySerializer(availability_details,data = request.data, many = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        availability_details = ClinicUser.objects.get(user = request.user)
        availability_details = availability_details.clinic.availability
        serializer = ClinicAvailabilitySerializer(availability_details, many = False)
        return Response(serializer.data)
class BufferTimeView(APIView):
    def post(self, request):
        serializer = BufferTimeSerializer(data = request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        serializer = BufferTimeSerializer(data = request.data, many=True)
        if serializer.is_valid():
            clinic_user_details = ClinicUser.objects.get(user = request.user)
            appointment_settings_details = clinic_user_details.clinic.appointment_settings
            buffer_times = BufferTime.objects.filter(appointment = appointment_settings_details)
            buffer_times.delete()
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        clinic_user_details = ClinicUser.objects.get(user = request.user)
        appointment_settings_details = clinic_user_details.clinic.appointment_settings
        buffer_times = BufferTime.objects.filter(appointment = appointment_settings_details)
        serializer = BufferTimeSerializer(buffer_times, many = True)
        return Response(serializer.data)

class Register(APIView):

    def post(self, request):
        serializer = UserSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
