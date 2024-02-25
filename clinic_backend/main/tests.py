from django.test import TestCase
import requests

# Create your tests here.
url = "http://localhost:8000/api/patient/"

res = requests.post(url, data = {
    'first_name': 'Emad',
})


print(res.status_code)