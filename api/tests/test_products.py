import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from ..models import Product


UserModel = get_user_model()


class APIAdminAPITestCase(APITestCase):
    @pytest.mark.django_db
    def setUp(self):
        self.user = UserModel.objects.create_superuser(
            username='test', email='test@est@testmail.com', password='top_secret')
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        print(token)


class APIUserAPITestCase(APITestCase):
    @pytest.mark.django_db
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='test', email='test@testmail.com', password='top_secret')
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        print("Token created",token)

        # Create a product
        url = ('/api/products/')
        data = {
            "product_name": "Test Product",
            "product_description": "Best product in town",
            "product_price": 10,
            "product_quantity": 5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'A product has been created')
        response = self.client.get('/api/products/product-list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'A product exists')


    # @pytest.mark.django_db
    # def test_can_get_product_list(self):
    #     # url = reverse('product-list')
    #     response = self.client.get('/api/products/product-list/')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, 'no products in the list')

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
