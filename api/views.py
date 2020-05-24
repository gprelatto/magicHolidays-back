from .models import *
from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.decorators import action
from django.db.models import Max
import django_filters

class userTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [HasAPIKey | IsAuthenticated]
    queryset = user_type.objects.all()
    serializer_class = userTypeSerializer


class countryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [HasAPIKey | IsAuthenticated]
    queryset = country.objects.all()
    serializer_class = countrySerializer


class userViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [HasAPIKey | IsAuthenticated]
    queryset = user.objects.all()
    serializer_class = userSerializer


class supplierViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [HasAPIKey | IsAuthenticated]
    queryset = supplier.objects.all()
    serializer_class = supplierSerializer


class productCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [HasAPIKey | IsAuthenticated]
    queryset = product_category.objects.all()
    serializer_class = productCategorySerializer

class productViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [HasAPIKey | IsAuthenticated]
    queryset = product.objects.all()
    serializer_class = productSerializer


class customerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [HasAPIKey | IsAuthenticated]
    queryset = customer.objects.all()
    serializer_class = customerSerializer


class paymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [HasAPIKey | IsAuthenticated]
    queryset = payment.objects.all()
    serializer_class = paymentSerializer

class rezViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [HasAPIKey | IsAuthenticated]
    queryset = rez.objects.all()
    serializer_class = rezSerializer


class auditViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [HasAPIKey | IsAuthenticated]
    queryset = audit.objects.all()
    serializer_class = auditSerializer

