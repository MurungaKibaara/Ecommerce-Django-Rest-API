from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Product
from .serializers import ProductSerializer

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Product.objects.filter(owner=user)
        raise PermissionDenied()

    # Set user as owner of a Product object.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
