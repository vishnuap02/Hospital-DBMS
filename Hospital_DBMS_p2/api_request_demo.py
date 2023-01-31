from flask import *
import requests

response = requests.get('http://127.0.0.1:5000/index')
print(response.status_code)
print(response.json())