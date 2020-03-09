from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from .models import Product, Order, Sale, Category
from rest_framework import filters
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

    serializer_class = ProductSerializer
    permission_classes = (IsOwner,)
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        'Wholesalers and Manufacturers can only view the products they own.'

        user = self.request.user
        if user.is_authenticated:
            if user.role == 'customer' or user.role == 'trader':
                queryset = Product.objects.all()
                serializer_class = ProductSerializer
                filter_backends = [DjangoFilterBackend]
                filterset_fields = ['pproduct_name', 'product_price']
                return Product.objects.all()
            return Product.objects.filter(owner=user)
        raise PermissionDenied()


    def perform_create(self, serializer):
        ''' Wholesalers and manufacturers can create products '''

        user = self.request.user
        if user.is_authenticated:
            if user.role == 'customer' or user.role == 'trader':
                raise PermissionDenied()
                return False
            return serializer.save(owner=self.request.user)
        raise PermissionDenied()

class OrderViewSet(viewsets.ModelViewSet):
    'Customers and small traders can only view the Orders they have created, while manufacturers and wholesalers cannot create orders.'

    serializer_class = OrderSerializer
    permission_classes = (IsOwner,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
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
