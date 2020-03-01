import json
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from ..models import Product


UserModel = get_user_model()

class TestProduct(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_data = {
        	"role":"manufacturer",
        	"email":"murungaephantus@gmail.com",
        	"username":"murungaephantus",
        	"name":"Murunga Kibaara",
        	"password":"securepassword",
        	"password2":"securepassword"
        }


        self.user_data_no_key = {
        	"email":"murungaephantus@gmail.com",
        	"username":"murungaephantus",
        	"name":"Murunga Kibaara",
        	"password":"securepassword",
        	"password2":"securepassword"
        }

        self.user_data_invalid_email = {
        	"role":"manufacturer",
        	"email":"murungaephantus",
        	"username":"murungaephantus",
        	"name":"Murunga Kibaara",
        	"password":"securepassword",
        	"password2":"securepassword"
        }

        self.user_data_wrong_password = {
        	"role":"manufacturer",
        	"email":"murungaephantus@gmail.com",
        	"username":"murungaephantus",
        	"name":"Murunga Kibaara",
        	"password":"securepassw",
        	"password2":"securepassword"
        }

        self.user_data_no_password = {
        	"role":"manufacturer",
        	"email":"murungaephantus@gmail.com",
        	"username":"murungaephantus",
        	"name":"Murunga Kibaara",
        	"password":"",
        	"password2":"securepassword"
        }

        self.user_data_no_all_password = {
        	"role":"manufacturer",
        	"email":"murungaephantus@gmail.com",
        	"username":"murungaephantus",
        	"name":"Murunga Kibaara",
        	"password":"",
        	"password2":""
        }

        self.login_data = {
        	"email":"murungaephantus@gmail.com",
        	"password":"securepassword",
        }

        self.login_data_no_key = {
        	"email":"murungaephantus@gmail.com",
        }

        self.login_data_wrong_password = {
        	"email":"murungaephantus@gmail.com",
        	"password":"securepassw",
        }

        # self.user_data = {"username": "test@testmail.com", "email": "test@testmail.com","password": "test","password2": "test"}
        self.product_data = {"product_id":1, "product_name": "Test Product","product_description": "Best product in town","product_price": 10,"product_quantity": 5}

    @pytest.mark.django_db
    def create_user(self):
        response = self.client.post('/api/accounts/register/',data=json.dumps(self.user_data),content_type='application/json')
        token = response.data['access']
        return token

    @pytest.mark.django_db
    def test_can_create_user(self):
        create_user_response = self.client.post('/api/accounts/register/',data=json.dumps(self.user_data),content_type='application/json')
        self.assertEqual(create_user_response.status_code, status.HTTP_201_CREATED, 'A user can be registered')

    @pytest.mark.django_db
    def test_can_create_user_key_missing(self):
        create_user_response = self.client.post('/api/accounts/register/',data=json.dumps(self.user_data_no_key),content_type='application/json')
        self.assertEqual(create_user_response.status_code, status.HTTP_400_BAD_REQUEST, 'A key is missing')

    @pytest.mark.django_db
    def test_can_create_user_unmatched_password(self):
        create_user_response = self.client.post('/api/accounts/register/',data=json.dumps(self.user_data_wrong_password),content_type='application/json')
        self.assertEqual(create_user_response.status_code, status.HTTP_400_BAD_REQUEST, 'Passwords did not match')

    @pytest.mark.django_db
    def test_can_create_user_invalid_email(self):
        create_user_response = self.client.post('/api/accounts/register/',data=json.dumps(self.user_data_invalid_email),content_type='application/json')
        self.assertEqual(create_user_response.status_code, status.HTTP_400_BAD_REQUEST, 'Invalid email')

    @pytest.mark.django_db
    def test_can_create_user_no_password(self):
        create_user_response = self.client.post('/api/accounts/register/',data=json.dumps(self.user_data_no_password),content_type='application/json')
        self.assertEqual(create_user_response.status_code, status.HTTP_400_BAD_REQUEST, 'No password')

    @pytest.mark.django_db
    def test_can_create_user_no_all_password(self):
        create_user_response = self.client.post('/api/accounts/register/',data=json.dumps(self.user_data_no_all_password),content_type='application/json')
        self.assertEqual(create_user_response.status_code, status.HTTP_400_BAD_REQUEST, 'No password')

    @pytest.mark.django_db
    def test_can_login_created_user(self):
        self.create_user()
        response = self.client.post('/api/accounts/token/',data=json.dumps(self.login_data),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'A user can be logged in')

    @pytest.mark.django_db
    def test_can_login_created_user_wrong_password(self):
        self.create_user()
        response = self.client.post('/api/accounts/token/',data=json.dumps(self.login_data_wrong_password),content_type='application/json')
        print("Status code", response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'Wrong password')

    @pytest.mark.django_db
    def test_can_login_created_user_no_key(self):
        self.create_user()
        response = self.client.post('/api/accounts/token/',data=json.dumps(self.login_data_no_key),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'No key')
