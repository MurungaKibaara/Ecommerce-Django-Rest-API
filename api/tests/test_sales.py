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

class TestSales(APITestCase):
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

        self.user2_data = {
        	"role":"trader",
        	"email":"murungaephantusk@gmail.com",
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

        self.sale_data = {
        	"order_id": 1,
            "order_status": "confirmed",
            "reference": 111
        }

        self.sale_data_no_key = {
            "order_status": "confirmed",
            "reference": 111
        }

        self.sale_data_update = {
        	"order_id": 1,
            "order_status": "cancelled",
            "reference": 130
        }

    @pytest.mark.django_db
    def test_not_create_sale_not_logged_in(self):

        user = mixer.blend('accounts.User',email='test@test.com', role='manufacturer', password='test',password2='test')
        customer = mixer.blend('accounts.User', role='customer', password='test',password2='test')
        product = mixer.blend('api.Product', owner=user)
        order = mixer.blend('api.Order', Product=product, owner=customer)

        datas = json.dumps(self.user_login_data)

        response = self.client.post('/api/sales/', self.sale_data, format='json')
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_not_get_sale_data_not_logged_in(self):

        user = mixer.blend('accounts.User',email='test@test.com', role='manufacturer', password='test',password2='test')
        customer = mixer.blend('accounts.User', role='customer', password='test',password2='test')
        product = mixer.blend('api.Product', owner=user)
        order = mixer.blend('api.Order', Product=product, owner=customer)

        response = self.client.get('/api/sales/')
        assert response.status_code == 403

        @pytest.mark.django_db
        def test_not_create_sale_key_missing(self):
            user = mixer.blend('accounts.User',email='test@test.com', role='manufacturer', password='test',password2='test')
            customer = mixer.blend('accounts.User', role='customer', password='test',password2='test')
            product = mixer.blend('api.Product', owner=user)
            order = mixer.blend('api.Order', Product=product, owner=customer)

            datas = json.dumps(self.user_login_data)

            response = self.client.post('/api/sales/', self.sale_data_no_key, format='json')
            assert response.status_code == 400
