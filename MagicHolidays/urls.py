"""MagicHolidays URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers
from api import views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'users', views.userViewSet)
router.register(r'userTypes', views.userTypeViewSet)
router.register(r'countries', views.countryViewSet)
router.register(r'suppliers', views.supplierViewSet)
router.register(r'productCategories', views.productCategoryViewSet)
router.register(r'products', views.productViewSet)
router.register(r'customers', views.customerViewSet)
router.register(r'payments', views.paymentViewSet)
router.register(r'reservations', views.rezViewSet)
router.register(r'audit', views.auditViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', views.LoginView.as_view(), name='login'),
    path('getProfile/', views.getProfileView.as_view(), name='profile'),    
    path('updatePassword/', views.updatePasswordView.as_view(), name='updatePassword')    
]