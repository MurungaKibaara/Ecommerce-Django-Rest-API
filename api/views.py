from rest_framework import viewsets, permissions, generics
from rest_framework import parsers
from django.http import JsonResponse
from rest_framework import status
# from rest_framework.generics import createAPIView
from rest_framework.parsers import FormParser,MultiPartParser, FileUploadParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from .models import Product, Order, Sale, Category
from rest_framework import filters
from rest_framework.response import Response
from .serializers import ProductSerializer, OrderSerializer, SaleSerializer, CategorySerializer

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class CategoryViewSet(viewsets.ModelViewSet):

    serializer_class = CategorySerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        'All authenticated users can view all categories'

        if  getattr(self, 'swagger_fake_view', False):
            return Category.objects.none()

        user = self.request.user
        if user.is_authenticated:
            return Category.objects.all()
        raise PermissionDenied()


    def perform_create(self, serializer):
        ' Only the product owners can create categories '

        user = self.request.user
        if user.is_authenticated:
            if user.role == 'customer' or user.role == 'trader':
                raise PermissionDenied()
                return False
            return serializer.save(owner=self.request.user)
        raise PermissionDenied()


class ProductViewSet(viewsets.ModelViewSet):
# class ProductViewSet(generics.ListCreateAPIView):

    serializer_class = ProductSerializer
    permission_classes = (IsOwner,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    # parser_classes = (MultiPartParser,FormParser,JSONParser, FileUploadParser)

    def get_queryset(self):
        'Wholesalers and Manufacturers can only view the products they own.'

        if  getattr(self, 'swagger_fake_view', False):
            return Product.objects.none()

        user = self.request.user
        if user.is_authenticated:
            if user.role == 'customer' or user.role == 'trader':
                queryset = Product.objects.all()
                serializer_class = ProductSerializer
                filter_backends = [DjangoFilterBackend]
                filterset_fields = ['product_name', 'product_price']
                return Product.objects.all()
            return Product.objects.filter(owner=user)
        raise PermissionDenied()

    def perform_create(self, serializer, format=None):
        serializer = ProductSerializer()
        parser_classes = (MultiPartParser, JSONParser)

        serializer = ProductSerializer(data=self.request.data)
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'customer' or user.role =='trader':
                raise PermissionDenied()
            if serializer.is_valid():
                serializer.save(owner=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise PermissionDenied()



    # def perform_create(self, serializer, request, format=None):
    # # def post(self, request, format=None):
    # # def post(self, request, format=None):
    #     serializer = ProductSerializer(data=self.request.DATA, files=self.request.FILES)
    #     # serializer = ProductSerializer(data=serializer.data['image']['image'])
    #     user = self.request.user
    #     print("Data", self.request.DATA, "Files", self.request.FILES)
    #
    #     if user.is_authenticated:
    #         if user.role == 'customer' or user.role =='trader':
    #             raise PermissionDenied()
    #         if serializer.is_valid():
    #
    #             print(serializer.data)
    #             return serializer.save(owner=user)
    #         return serializer.errors
    #     raise PermissionDenied()


class OrderViewSet(viewsets.ModelViewSet):
    'Customers and small traders can only view the Orders they have created, while manufacturers and wholesalers cannot create orders.'

    serializer_class = OrderSerializer
    permission_classes = (IsOwner,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        if  getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()

        user = self.request.user
        if user.is_authenticated:
            if user.role == 'manufacturer' or user.role == 'wholesaler':
                return Order.objects.filter(product_id__owner=user)
            return Order.objects.filter(owner=user)
        raise PermissionDenied()


    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'manufacturer' or user.role == 'wholesaler':
                raise PermissionDenied()
            return serializer.save(owner=self.request.user)
        raise PermissionDenied()


class SaleViewSet(viewsets.ModelViewSet):
    'Only product owners can confirm orders'

    serializer_class = SaleSerializer
    permission_classes = (IsOwner,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if  getattr(self, 'swagger_fake_view', False):
            return Sale.objects.none()

        user = self.request.user
        if user.is_authenticated:
            if user.role != 'manufacturer' or user.role != 'trader':
                return Sale.objects.filter(order_id__product_id__owner=user)
            raise PermissionDenied()
        raise PermissionDenied()

    def perform_create(self, serializer):
        user = self.request.user
        data=serializer.validated_data
        if user.is_authenticated:
            if user.role == 'manufacturer' or user.role == 'wholesaler':
                orders = Order.objects.filter(product_id__owner=user)
                for order in orders:
                    print("Order Numbers",order.order, data['order_id'])
                    if order.order != data['order_id'] and order.order_status != 'cancelled':
                        return
                    return serializer.save(owner=self.request.user)
            raise PermissionDenied()
        raise PermissionDenied()
