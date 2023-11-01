from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework import status
import jwt
from users.models import *

JWT_SECRET_KEY = getattr(settings, 'SECRET_KEY', None)


def decode_token(encoded_jwt):
    decoded_jwt = jwt.decode(encoded_jwt, JWT_SECRET_KEY, algorithms=['HS256'])
    return decoded_jwt


class UserRegisterViewTest(TestCase):
    
    def setUp(self):
        #noheaders needed when registering 
        self.client = APIClient()
        self.headers = {}
        self.client.credentials(**self.headers)
        
    def test_valid_credentials(self):
        response = self.client.post(
            reverse('users:register'),
            {'username': 'eddy', 'email': 'test@test.com', 'password': 'testpass', 'role': 'customer'}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.json())
        
        
class LoginViewTest(TestCase):
    def setUp(self):
        #noheaders needed when registering 
        self.client = APIClient()
        self.user = User.objects.create(
            username='testuser',
            email='test@test.com'
        )
        
        self.user.set_password('password')
        self.user.save()
        
        self.headers = {}
        self.client.credentials(**self.headers)
        
        
    def test_user_login_valid_credentials(self):
        response = self.client.post(
            reverse('users:login'),
            {'email': 'test@test.com', 'password': 'password'}
        )
        
        
        decoded_useer_id = decode_token(response.json()['token'])['id']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.json())
        self.assertEqual(decoded_useer_id, str(self.user.id))
    