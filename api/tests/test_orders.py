import json
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from mixer.backend.django import mixer
from ..models import Product


UserModel = get_user_model()

class TestOrders(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_data = {
        	"role":"manufacturer",
        	"email":"murungaephantus@gmail.com",
        	"username":"murungaephantus",
        	"name":"Murunga Kibaara",
        	"password":"securepassword",
        	"password2":"securepassword",
            "region":"Nairobi"
        }

        self.user_login_data = {
            "email":"test@test.com",
            "password":"test",
        }

        self.user2_data = {
        	"role":"trader",
        	"email":"murungaephantusk@gmail.com",
        	"username":"murungaephantus",
        	"name":"Murunga Kibaara",
        	"password":"securepassword",
        	"password2":"securepassword",
            "region":"Nairobi"
        }

        self.product_data = {
        	"product_name": "5KG Sugar",
            "product_description": "Mumias Sugar",
            "product_price": 110,
            "product_quantity": 200
        }

        self.order_data = {
        	"product_id": 1,
            "order_status": "cart",
            "product_price": 110,
            "order_quantity": 200
        }

        self.order_data_key_missing = {
            "order_status": "cart",
            "product_price": 110,
            "order_quantity": 200
        }

        self.sale_data = {
        	"order_id": 1,
            "order_status": "confirmed",
            "reference": 111
        }

        self.sale_data_no_key = {
        	"order_id": 1,
            "order_status": "confirmed",
            "reference": 111
        }

        self.sale_data_update = {
        	"order_id": 1,
            "order_status": "cancelled",
            "reference": 130
        }

    @pytest.mark.django_db
    def test_not_create_order_not_logged_in(self):

        user = mixer.blend('accounts.User',email='test@test.com', role='manufacturer', password='test',password2='test')
        customer = mixer.blend('accounts.User', role='customer', password='test',password2='test')
        product = mixer.blend('api.Product', owner=user)

        response = self.client.post('/api/v1/orders/', self.order_data, format='json')
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_not_get_order_data_not_logged_in(self):

        user = mixer.blend('accounts.User',email='test@test.com', role='manufacturer', password='test',password2='test')
        customer = mixer.blend('accounts.User', role='customer', password='test',password2='test')
        product = mixer.blend('api.Product', owner=user)

        response = self.client.get('/api/v1/orders/')
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_not_create_order_key_missing(self):

        user = mixer.blend('accounts.User',email='test@test.com', role='manufacturer', password='test',password2='test')
        customer = mixer.blend('accounts.User', role='customer', password='test',password2='test')
        product = mixer.blend('api.Product', owner=user)

        response = self.client.post('/api/v1/orders/', self.order_data_key_missing, format='json')
        assert response.status_code == 400
