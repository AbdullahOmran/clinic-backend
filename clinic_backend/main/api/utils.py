from rest_framework_simplejwt.tokens import AccessToken

def get_payload(request):
    access_token = request.headers.get('Authorization')[7:]
    decoded_token = AccessToken(access_token).payload
    return decoded_token

