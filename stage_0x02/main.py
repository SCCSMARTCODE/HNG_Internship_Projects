import requests
import json
import pprint

url = "https://hng-internship-projects-r1b1.vercel.app/api/users/fd1087e5-acd1-47e4-9079-3564b6847c3d"
# ''
payload = {'email': 'sccsmart417@gmail.com', 'password': 'mightysmart', 'firstName': 'EMMANUEL', 'lastName': 'AYOBAMI', 'name': 'new Organisation', 'description': 'new new', }
headers = {'Content-Type': 'application/json', 'Authorization': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZmQxMDg3ZTUtYWNkMS00N2U0LTkwNzktMzU2NGI2ODQ3YzNkIiwiZXhwIjoxNzIwNjg4Mjc1fQ._RvEp8dS_zmBT-fMcjkhrDEdskxfbPDDyRGjMHAQwHQ"}

response = requests.get(url, data=json.dumps(payload), headers=headers)

pprint.pprint(response.content)


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZmQxMDg3ZTUtYWNkMS00N2U0LTkwNzktMzU2NGI2ODQ3YzNkIiwiZXhwIjoxNzIwNzczNzQ1fQ.UqDnQCBcS4MuWDI5d-Oxd1IDO4bW-TYMUwuV1l2xcj0
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZmQxMDg3ZTUtYWNkMS00N2U0LTkwNzktMzU2NGI2ODQ3YzNkIiwiZXhwIjoxNzIwNjg3Njk5fQ.f3iH8WCvIK3dteQkfdNrAq8GdyzVcUW3z3jSqJlFXgg
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZmQxMDg3ZTUtYWNkMS00N2U0LTkwNzktMzU2NGI2ODQ3YzNkIiwiZXhwIjoxNzIwNjg4Mjc1fQ._RvEp8dS_zmBT-fMcjkhrDEdskxfbPDDyRGjMHAQwHQ
