from rest_framework_simplejwt.tokens import AccessToken
from ..models import Secretary, Doctor

def get_payload(request):
    access_token = request.headers.get('Authorization')[7:]
    decoded_token = AccessToken(access_token).payload
    return decoded_token

def get_staff_obj(request):
    doctors = Patient.objects.filter(user = request.user)
    secretaries = Secretary.objects.filter(user = request.user)
    if doctors.count() > 0:
        return doctors[0]
    if secretaries.count()>0:
        return secretaries[0]
