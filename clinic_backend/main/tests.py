from django.test import TestCase
import requests

# Create your tests here.
url = "http://localhost:8000/api/patient/4/"

res = requests.get(url)


print(res.status_code)