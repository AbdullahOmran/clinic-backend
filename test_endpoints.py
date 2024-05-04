# Create your tests here.
import requests


class TestAPIClient(object):
    
    def __init__(self):
        self.BASE_URL = 'http://localhost:8000/api'

        self.endpoints = {
            'login':f'{self.BASE_URL}/auth/login/',
            'appointment-settings':f'{self.BASE_URL}/appointment-settings/',
           
            
            
        }

        res = requests.post(self.reverse('login'), data={
            'username': 'AbdullahOmran',
            'password': '123456789',
        })
        access_token = None
        if res.status_code == 200:
           access_token = res.json().get('access')

        self.headers = {
            'Authorization': 'Bearer '+ access_token
        }

    def reverse(self,endpoint):
        return self.endpoints.get(endpoint)

    def test_create_appointment_settings(self):
        res = requests.post(self.reverse('appointment-settings'), headers=self.headers,data={
            "max_appointments": 2,
            "duration": 20,
        })

APIClient = TestAPIClient()
APIClient.test_create_appointment_settings()