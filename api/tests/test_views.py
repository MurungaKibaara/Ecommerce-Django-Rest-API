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

        # self.user_data = {"username": "test@testmail.com", "email": "test@testmail.com","password": "test","password2": "test"}
        self.product_data = {"product_id":1, "product_name": "Test Product","product_description": "Best product in town","product_price": 10,"product_quantity": 5}

    @pytest.mark.django_db
    def create_user(self):
        response = self.client.post('/api/accounts/register/',data=json.dumps(self.user_data),content_type='application/json')
        token = response.data['access']
        return token

    @pytest.mark.django_db
    def test_a_registered_user_can_create_a_product(self):
        token = self.create_user()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        response = self.client.post('/api/products/', data=json.dumps(self.product_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'A product has been created')

    @pytest.mark.django_db
    def test_can_get_created_products(self):
        token = self.create_user()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        self.client.post('/api/products/', data=json.dumps(self.product_data), content_type='application/json')
        product_resp = self.client.get('/api/products/')
        self.assertEqual(product_resp.status_code, status.HTTP_200_OK, 'A product exists')






































# @pytest.mark.django_db
# def test_can_get_product_list(self):
#     # url = reverse('product-list')
#     response = self.client.get('/api/products/product-list/')
#     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, 'no products in the list')


# class APIAdminAPITestCase(APITestCase):
#     @pytest.mark.django_db
#     def setUp(self):
#         self.user = UserModel.objects.create_superuser(
#             username='test', email='test@est@testmail.com', password='top_secret')
#         token = Token.objects.create(user=self.user)
#         self.client = APIClient()
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
#         print(token)
#


#
# class TestProductList(APITestCase):
#     @pytest.mark.django_db
#     def test_can_get_product_list(self):
#         # url = reverse('api:product-list')
#         response = self.client.get('/api/products/product-list/')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, 'no products in the list')
#
#     @pytest.mark.django_db
#     def test_can_create_product(self):
#         # url = reverse('api:product-list')
#         response = self.client.get('/api/products/product-list/')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, 'no products in the list')
