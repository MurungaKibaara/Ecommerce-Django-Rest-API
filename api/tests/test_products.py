import io
import json
import base64
import pytest
import numpy

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from io import BytesIO

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


# Mock Image
from PIL import Image, ImageDraw
from base64 import decodestring

# Local Import
from ..models import Product


UserModel = get_user_model()

# TODO: UPDATE CATEGORY INFORMATION IN TESTS

class TestProduct(APITestCase):
    def setUp(self):

        self.url = '/api/v1/products'
        self.product_url = '/api/v1/products/1'

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

        self.user3_data = {
        	"role":"customer",
        	"email":"murungaephantusk@gmail.com",
        	"username":"murungaephantus",
        	"name":"Murunga Kibaara",
        	"password":"securepassword",
        	"password2":"securepassword",
            "region":"Nairobi"
        }

        self.user2_data = {
        	"role":"manufacturer",
        	"email":"murungakibaara@gmail.com",
        	"username":"murungaephantus",
        	"name":"Murunga Kibaara",
        	"password":"securepassword",
        	"password2":"securepassword",
            "region":"Nairobi"
        }

        self.user4_data = {
        	"role":"trader",
        	"email":"murungakibaara@gmail.com",
        	"username":"murungaephantus",
        	"name":"Murunga Kibaara",
        	"password":"securepassword",
        	"password2":"securepassword",
            "region":"Nairobi"
        }

        self.user5_data = {
        	"role":"wholesaler",
        	"email":"murungakibaara@gmail.com",
        	"username":"murungaephantus",
        	"name":"Murunga Kibaara",
        	"password":"securepassword",
        	"password2":"securepassword",
            "region":"Nairobi"
        }

        self.category_data  ={
        "name":"Food Items",
        }



        # Products Data including Image Data

        with open('/home/murunga/Desktop/image.jpg', 'rb') as img1:

            imgStringIO1 = Image.open(BytesIO(img1.read()))

            self.product_data = {
                "category":1,
            	"product_name": "1KG Sugar",
                "product_description": "Mumias Sugar",
                "product_price": 198,
                "product_quantity": 200,
                "image": (imgStringIO1)
            }

            self.product_data_no_key = {
                "category":1,
                "product_description": "Mumias Sugar",
                "product_price": 500,
                "product_quantity": 200,
                "image": (imgStringIO1)
            }

            self.product_data_update = {
                "category":1,
            	"product_name": "1KG Sugar",
                "product_description": "Mumias Sugar",
                "product_price": 500,
                "product_quantity": 200,
                "image": (imgStringIO1)
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
    def create_user3(self):
        response = self.client.post('/api/accounts/register/',data=json.dumps(self.user3_data),content_type='application/json')
        token = response.data['access']
        return token

    @pytest.mark.django_db
    def create_user4(self):
        response = self.client.post('/api/accounts/register/',data=json.dumps(self.user4_data),content_type='application/json')
        token = response.data['access']
        return token

    @pytest.mark.django_db
    def create_user5(self):
        response = self.client.post('/api/accounts/register/',data=json.dumps(self.user5_data),content_type='application/json')
        token = response.data['access']
        return token

    # @pytest.mark.django_db
    # def test_a_registered_user_can_create_a_product(self):
    #     token = self.create_user()
    #     self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
    #
    #     resp = self.client.post('/api/v1/categories/', data=json.dumps(self.category_data), content_type='application/json')
    #     response = self.client.post(self.url, data=self.product_data, format='multipart', follow=True)
    #
    #     # import pdb; pdb.set_trace()
    #     # response = self.client.get(self.url, follow=True)
    #     last_url, status_code = response.redirect_chain[-1]
    #     print(response.redirect_chain, last_url, status_code)
    #     # print("Response", response.data['results'])
    #     self.assertEqual(response.status_code,  201, 'A product has been created')
    #     # self.assertContains(response, 'product does not exist',status_code=404)

    # @pytest.mark.django_db
    # def test_can_get_created_products(self):
    #     token = self.create_user()
    #     self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
    #     self.client.post('/api/v1/categories/', data=json.dumps(self.category_data), content_type='application/json')
    #     self.client.post(self.url, data=self.product_data, content_type='multipart/form-data', follow=True)
    #     product_resp = self.client.get(self.url)
    #     self.assertEqual(product_resp.status_code, status.HTTP_200_OK, 'A product exists')

    @pytest.mark.django_db
    def test_dont_update_products_that_dont_exist(self):
        token = self.create_user()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        self.client.post('/api/v1/categories/', data=json.dumps(self.category_data), content_type='application/json')
        product_resp = self.client.put(self.product_url, data=self.product_data, content_type='multipart/form-data', follow=True)
        self.assertEqual(product_resp.status_code, status.HTTP_404_NOT_FOUND, 'Product does not exist')
    # #
    # @pytest.mark.django_db
    # def test_can_update_existing_products(self):
    #     token = self.create_user()
    #     self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
    #     self.client.post('/api/v1/categories/', data=json.dumps(self.category_data), content_type='application/json')
    #     response = self.client.post(self.url, data=self.product_data, content_type='multipart/form-data', follow=True)
    #     product_resp = self.client.put(self.product_url, data=self.product_data_update, content_type='multipart/form-data', follow=True)
    #     self.assertEqual(product_resp.status_code, status.HTTP_200_OK, 'Product can be updated')

    @pytest.mark.django_db
    def test_dont_create_with_missing_key(self):
        token = self.create_user()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        self.client.post('/api/v1/categories/', data=json.dumps(self.category_data), content_type='application/json')
        product_resp = self.client.post('/api/v1/products/', data=self.product_data_no_key, content_type='multipart/form-data', follow=True)
        self.assertEqual(product_resp.status_code, status.HTTP_400_BAD_REQUEST, 'Product can be updated')

    @pytest.mark.django_db
    def test_non_logged_in_cant_create(self):
        product_resp = self.client.post('/api/v1/products/', data=self.product_data_no_key, content_type='multipart/form-data', follow=True)
        self.assertEqual(product_resp.status_code, status.HTTP_400_BAD_REQUEST, 'Non user cant create products')

    @pytest.mark.django_db
    def test_empty_returns_404(self):
        token = self.create_user()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        product_resp = self.client.get('/api/v1/products/1/')
        self.assertEqual(product_resp.status_code, status.HTTP_404_NOT_FOUND, 'Product can be updated')

    # @pytest.mark.django_db
    # def test_return_one_product(self):
    #     token = self.create_user()
    #     self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
    #     self.client.post('/api/v1/categories/', data=json.dumps(self.category_data), content_type='application/json')
    #     self.client.post('/api/v1/products/', data=self.product_data, content_type='multipart/form-data', follow=True)
    #     product_resp = self.client.get('/api/v1/products/1/')
    #     self.assertEqual(product_resp.status_code, status.HTTP_200_OK, 'Product can be updated')

    @pytest.mark.django_db
    def test_different_product_owners_read(self):
        token = self.create_user()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        self.client.post('/api/v1/categories/', data=json.dumps(self.category_data), content_type='application/json')
        self.client.post('/api/v1/products/', data=self.product_data, content_type='multipart/form-data', follow=True)

        token2 = self.create_user2()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token2)

        product_resp = self.client.get('/api/v1/products/1/')
        self.assertEqual(product_resp.status_code, status.HTTP_404_NOT_FOUND, 'A user cannot access another users products')

    @pytest.mark.django_db
    def test_diffrent_product_owners_update(self):
        token = self.create_user()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        self.client.post('/api/v1/categories/', data=json.dumps(self.category_data), content_type='application/json')
        self.client.post('/api/v1/products/', data=self.product_data, content_type='multipart/form-data', follow=True)

        token2 = self.create_user2()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token2)

        product_resp = self.client.put('/api/v1/products/1/', data=self.product_data, content_type='multipart/form-data', follow=True)
        self.assertEqual(product_resp.status_code, status.HTTP_404_NOT_FOUND, 'A user cannot update another users products')

    # @pytest.mark.django_db
    # def test_a_user_can_delete_a_product(self):
    #     token = self.create_user()
    #     self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
    #     self.client.post('/api/v1/categories/', data=json.dumps(self.category_data), content_type='application/json')
    #     response= self.client.post(self.url, data=self.product_data, content_type='multipart/form-data', follow=True)
    #     product_resp = self.client.delete(self.product_url, follow=True)
    #     self.assertEqual(product_resp.status_code, status.HTTP_204_NO_CONTENT, 'A user can delete a product')

    @pytest.mark.django_db
    def test_delete_different_owner_products(self):
        token = self.create_user()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        self.client.post('/api/v1/categories/', data=json.dumps(self.category_data), content_type='application/json')
        self.client.post('/api/v1/products/', data=self.product_data, content_type='multipart/form-data', follow=True)

        token2 = self.create_user2()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token2)

        product_resp = self.client.delete('/api/v1/products/1/', data=self.product_data, content_type='multipart/form-data', follow=True)
        self.assertEqual(product_resp.status_code, status.HTTP_404_NOT_FOUND, 'A user cannot delete another users products')

    @pytest.mark.django_db
    def test_a_customer_cannot_create_a_product(self):
        token = self.create_user3()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        self.client.post('/api/v1/categories/', data=json.dumps(self.category_data), content_type='application/json')
        response = self.client.post('/api/v1/products/', self.product_data, content_type='multipart/form-data', follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'A product cannot be be created')
    #
    @pytest.mark.django_db
    def test_a_trader_cannot_create_a_product(self):
        token = self.create_user4()
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        self.client.post('/api/v1/categories/', data=json.dumps(self.category_data), content_type='application/json')
        response = self.client.post('/api/v1/products/', self.product_data, content_type='multipart/form-data', follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'A product cannot be be created')
    #
    # @pytest.mark.django_db
    # def test_a_wholesaler_can_create_a_product(self):
    #     token = self.create_user5()
    #     self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
    #     self.client.post('/api/v1/categories/', data=json.dumps(self.category_data), content_type='application/json')
    #     response = self.client.post('/api/v1/products/', data=self.product_data, content_type='multipart/form-data', follow=True)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'A product cannot be be created')
