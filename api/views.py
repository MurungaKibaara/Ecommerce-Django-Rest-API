from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Product, Order, Sale
from .serializers import ProductSerializer, OrderSerializer, SaleSerializer

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        '''
            - Customers and small traders can view all the Products.
            - Wholesalers and Manufacturers can only view the products they own.
        '''

        user = self.request.user
        if user.is_authenticated:
            if user.role == 'customer' or user.role == 'trader':
                return Product.objects.all()
            return Product.objects.filter(owner=user)
        raise PermissionDenied()


    def perform_create(self, serializer):
        ''' Customers and small traders cannot create Products '''

        user = self.request.user
        if user.is_authenticated:
            if user.role == 'customer' or user.role == 'trader':
                raise PermissionDenied()
                return False
            return serializer.save(owner=self.request.user)
        raise PermissionDenied()

class OrderViewSet(viewsets.ModelViewSet):
    '''
        - Customers and small traders can only view the products they have created.
        - Manufacturers and wholesalers cannot create orders.
    '''

    serializer_class = OrderSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'manufacturer' or user.role == 'wholesaler' or user.role == 'admin':
                return Order.objects.all()
            return Order.objects.filter(owner=user)
        raise PermissionDenied()


    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'manufacturer' or user.role == 'wholesaler':
                raise PermissionDenied()
                return False
            return serializer.save(owner=self.request.user)
        raise PermissionDenied()


class SaleViewSet(viewsets.ModelViewSet):
    '''
        - Customers and small traders can only view the products they have created.
        - Manufacturers and wholesalers cannot create orders.
    '''

    serializer_class = SaleSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'manufacturer' or user.role == 'wholesaler' or user.role == 'admin':
                return Sale.objects.all()
            return Sale.objects.filter(owner=user)
        raise PermissionDenied()


    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            if user.role == 'manufacturer' or user.role == 'wholesaler':
                raise PermissionDenied()
                return False
            return serializer.save(owner=self.request.user)
        raise PermissionDenied()
