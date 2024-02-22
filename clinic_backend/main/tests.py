from django.test import TestCase
import requests

# Create your tests here.
url = "http://localhost:8000/api/patient/1/"

res = requests.put(url, data = {'first_name':""})


print(res.status_code)