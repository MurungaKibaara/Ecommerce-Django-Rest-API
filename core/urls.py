"""core URL Configuration"""
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


schema_view = get_schema_view(
   openapi.Info(
      title="Smartsys e-retail API",
      default_version='v1',
      description="""eretail is an a django based application that links small traders and customers to different tiers of wholesalers and manufacturers on the same platform.
      It is driven by the need to cut customer acquisition costs for wholesalers and manufactures and thereby driving the product costs down for willing buyers.
      """,
      # terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="murungaephantus@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('auth/', include('rest_framework.urls')),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/accounts/', include('accounts.urls'), name='accounts'),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
