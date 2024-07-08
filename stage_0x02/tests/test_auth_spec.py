import time
import unittest
import json
import jwt
import datetime
import app
from model.engine import session
from model.user_model import UserModel
from model.organisation_model import OrganisationModel
from model.user_to_organisation_model import UserToOrganisationModel
from werkzeug.security import generate_password_hash
import uuid


class TestAuthEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app = app.test_client()
        self.app.testing = True
        self.session = session()
        self.secret_key = str(app.config['SECRET_KEY'])

    def tearDown(self):
        self.session.query(UserToOrganisationModel).delete()
        self.session.query(OrganisationModel).delete()
        self.session.query(UserModel).delete()
        self.session.commit()
        self.session.close()

    def test_register_success(self):
        response = self.app.post('/auth/register', data=json.dumps({
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123'
        }), content_type='application/json')

        print(response)

        if response.status_code != 201:
            print(f"Unexpected status code: {response.status_code}")
            print(f"Response data: {response.get_data(as_text=True)}")

        try:
            data = json.loads(response.get_data(as_text=True))
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {response.get_data(as_text=True)}")
            raise e

        self.assertEqual(response.status_code, 201)
        self.assertIn('accessToken', data.get('data'))


    def test_register_missing_fields(self):
        response = self.app.post('/auth/register', json={
            'firstName': 'John',
            'email': 'john.doe@example.com',
            'password': 'password123'
        })
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 422)
        self.assertIn('errors', data)

    def test_register_duplicate_email(self):
        user = UserModel(userId=str(uuid.uuid4()), firstName='John', lastName='Doe', email='john.doe@example.com', password='password123')
        self.session.add(user)
        self.session.commit()

        response = self.app.post('/auth/register', json={
            'firstName': 'Jane',
            'lastName': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'password123'
        })
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 422)
        self.assertIn('errors', data)

    def test_login_success(self):
        user = UserModel(userId=str(uuid.uuid4()), firstName='John', lastName='Doe', email='john.doe@example.com', password=generate_password_hash('password123', method='pbkdf2:sha256'))
        self.session.add(user)
        self.session.commit()

        response = self.app.post('/auth/login', json={
            'email': 'john.doe@example.com',
            'password': 'password123'
        })
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertIn('accessToken', data['data'])
        self.assertEqual(data['data']['user']['email'], 'john.doe@example.com')

    def test_login_fail(self):
        response = self.app.post('/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 401)

    def test_token_expiry(self):
        token = jwt.encode({'user_id': '12345', 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, self.secret_key)
        decoded = jwt.decode(token, self.secret_key, algorithms=['HS256'])
        self.assertIn('exp', decoded)
        self.assertIn('user_id', decoded)
        self.assertEqual(decoded['user_id'], '12345')

    def test_token_expiry_incorrect_time(self):
        token = jwt.encode({'user_id': '12345', 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1)}, self.secret_key)
        time.sleep(2)
        try:
            decoded = jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError as e:
            decoded = None
        self.assertEqual(None, decoded)

    def test_access_unauthorised_organisation(self):
        user1 = UserModel(userId=str(uuid.uuid4()), firstName='John', lastName='Doe', email='john.doe@example.com', password='password123')
        user2 = UserModel(userId=str(uuid.uuid4()), firstName='Jane', lastName='Doe', email='jane.doe@example.com', password='password123')
        self.session.add(user1)
        self.session.add(user2)
        self.session.commit()

        org1 = OrganisationModel(orgId=str(uuid.uuid4()), name="John's Organisation", description="")
        self.session.add(org1)
        self.session.commit()

        user_to_org1 = UserToOrganisationModel(userId=user1.userId, orgId=org1.orgId, isCreator=True)
        self.session.add(user_to_org1)
        self.session.commit()

        token = jwt.encode({'user_id': user2.userId, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, self.secret_key)
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.get(f'/api/organisations/{org1.orgId}', headers=headers)
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
