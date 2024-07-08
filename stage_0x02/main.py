import requests
import json
import pprint

url = 'https:/hng-internship-projects-4ypo.vercel.app/auth/register'
payload = {'email': 'sccsmart247@gmail.com', 'password': 'mightysmart', 'firstName': 'EMMANUEL', 'lastName': 'AYOBAMI', 'name': 'new Organisation', 'description': 'new new', }
headers = {'Content-Type': 'application/json', 'Authorization': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZTEwMmMxODQtNjU2YS00N2E1LTgxZmMtZDQwYThlNGExMjQzIiwiZXhwIjoxNzIwNDc1ODI1fQ.sED9OugV-svG0g8Zazwlb2C6DwLsCxlGVLoIfzXMykE"}

response = requests.post(url, data=json.dumps(payload), headers=headers)

pprint.pprint(response.content)
