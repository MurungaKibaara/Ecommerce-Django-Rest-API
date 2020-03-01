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

        self.user2_data = {
        	"role":"customer",
        	"email":"murungakibaara@gmail.com",
        	"username":"murungaephantus",
        	"name":"Murunga Kibaara",
        	"password":"securepassword",
        	"password2":"securepassword"
        }

        self.product_data = {
        	"product_name": "1KG Sugar",
            "product_description": "Mumias Sugar",
            "product_price": 198,
            "product_quantity": 200
        }

        self.product_data_no_key = {
            "product_description": "Mumias Sugar",
            "product_price": 500,
            "product_quantity": 200
        }

        self.product_data_update = {
        	"product_name": "1KG Sugar",
            "product_description": "Mumias Sugar",
            "product_price": 500,
            "product_quantity": 200
        }

    @pytest.mark.django_db
    def create_user(self):
        response = self.client.post('/api/accounts/register/',data=json.dumps(self.user_data),content_type='application/json')
        token = response.data['access']
        return token

    @pytest.mark.django_db
    def create_user2(self):
        response = self.client.post('/api/accounts/register/',data=json.dumps(self.user2_data),content_type='application/json')
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

    @pytest.mark.django_db
    def test_dont_update_products_that_dont_exist(self):
        token = self.create_user()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        product_resp = self.client.put('/api/products/1/', data=json.dumps(self.product_data), content_type='application/json')
        self.assertEqual(product_resp.status_code, status.HTTP_404_NOT_FOUND, 'Product does not exist')

    @pytest.mark.django_db
    def test_can_update_existing_products(self):
        token = self.create_user()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        self.client.post('/api/products/', data=json.dumps(self.product_data), content_type='application/json')
        product_resp = self.client.put('/api/products/1/', data=json.dumps(self.product_data_update), content_type='application/json')
        self.assertEqual(product_resp.status_code, status.HTTP_200_OK, 'Product can be updated')

    @pytest.mark.django_db
    def test_dont_create_with_missing_key(self):
        token = self.create_user()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        product_resp = self.client.post('/api/products/', data=json.dumps(self.product_data_no_key), content_type='application/json')
        self.assertEqual(product_resp.status_code, status.HTTP_400_BAD_REQUEST, 'Product can be updated')

    @pytest.mark.django_db
    def test_non_logged_in_cant_create(self):
        product_resp = self.client.post('/api/products/', data=json.dumps(self.product_data_no_key), content_type='application/json')
        self.assertEqual(product_resp.status_code, status.HTTP_400_BAD_REQUEST, 'Non user cant create products')

    @pytest.mark.django_db
    def test_empty_returns_404(self):
        token = self.create_user()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        product_resp = self.client.get('/api/products/1/')
        self.assertEqual(product_resp.status_code, status.HTTP_404_NOT_FOUND, 'Product can be updated')

    @pytest.mark.django_db
    def test_return_one_product(self):
        token = self.create_user()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        self.client.post('/api/products/', data=json.dumps(self.product_data), content_type='application/json')
        product_resp = self.client.get('/api/products/1/')
        self.assertEqual(product_resp.status_code, status.HTTP_200_OK, 'Product can be updated')

    @pytest.mark.django_db
    def test_diffrent_product_owners_read(self):
        token = self.create_user()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        self.client.post('/api/products/', data=json.dumps(self.product_data), content_type='application/json')

        token2 = self.create_user2()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token2)
        self.client.get('/api/products/')

        product_resp = self.client.get('/api/products/1/')
        self.assertEqual(product_resp.status_code, status.HTTP_404_NOT_FOUND, 'A user cannot access another users products')







































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
