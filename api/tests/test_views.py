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

        self.user_data = {"username": "test@testmail.com", "email": "test@testmail.com","password": "test","password2": "test"}
        self.product_data = {"product_id":1, "product_name": "Test Product","product_description": "Best product in town","product_price": 10,"product_quantity": 5}

    @pytest.mark.django_db
    def test_can_create_user(self):
        create_user_response = self.client.post('/api/jwtauth/register/',data=json.dumps(self.user_data),content_type='application/json')
        self.assertEqual(create_user_response.status_code, status.HTTP_201_CREATED, 'A user can be registered')

    @pytest.mark.django_db
    def test_can_login_created_user(self):
        create_user_response = self.client.post('/api/jwtauth/register/',data=json.dumps(self.user_data),content_type='application/json')

        response = self.client.post('/api/token/',data=json.dumps(self.user_data),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'A user can be logged in')

    @pytest.mark.django_db
    def test_a_registered_user_can_create_a_product(self):
        response = self.client.post('/api/jwtauth/register/',data=json.dumps(self.user_data),content_type='application/json')
        headers = {'HTTP_AUTHORIZATION': str(response.data['access'])}
        print("Header: ",headers)

        response = self.client.post('/api/products/', headers=headers, data=json.dumps(self.product_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'A product has been created')

    @pytest.mark.django_db
    def test_can_get_created_products(self):
        response = self.client.post('/api/jwtauth/register/', data=json.dumps(self.user_data),content_type='application/json')
        header = {"Authorization": response.data['access']}

        response = self.client.get('/api/products/product-list/', headers=header, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'A product exists')






































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
