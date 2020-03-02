from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import ProductViewSet, OrderViewSet

router = SimpleRouter()
router.register('products', ProductViewSet, basename='products')
router.register('orders', OrderViewSet, basename='orders')
urlpatterns = router.urls
