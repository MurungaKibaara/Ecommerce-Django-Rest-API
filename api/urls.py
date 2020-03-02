from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import ProductViewSet, OrderViewSet, SaleViewSet

router = SimpleRouter()
router.register('products', ProductViewSet, basename='products')
router.register('orders', OrderViewSet, basename='orders')
router.register('sales', SaleViewSet, basename='sales')
urlpatterns = router.urls
