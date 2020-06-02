from .models import *
from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from api.middlewareSecurity import checkAccess
from rest_framework.decorators import action
from django.db.models import Max
import django_filters
import hashlib 
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date
from django.shortcuts import get_object_or_404

class userTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess | IsAuthenticated]
    queryset = user_type.objects.all()
    serializer_class = userTypeSerializer

class LoginView(APIView):
    permission_classes = []
    queryset = user.objects.all()
    serializer_class = userSerializer

    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        fMail = request.data['mail']
        fPassword = request.data['password']
        ePassword = hashlib.md5(fPassword.encode()).hexdigest()
        request.data._mutable = False
        serializerform = loginSerializer(data=request.data)
        try:
            oUser = user.objects.get(mail = fMail)
            today = date.today()
            if ePassword == oUser.password :
                try:
                    obj = token.objects.get(user = oUser.id,date = today)
                    return Response({
                        "records": 1,
                        "code": 200,
                        "message": "Login exitoso, token en el result",
                        "results": [{
                                'token' : obj.token,
                                'mail' : oUser.mail,
                                'user_type' : oUser.user_type.id
                            }]                       
                    })               
                except token.DoesNotExist:
                    kToken = oUser.mail + oUser.password + str(today)
                    gToken = hashlib.md5(kToken.encode()).hexdigest()
                    cToken = token(date = today , user = oUser, token = gToken)
                    cToken.save()
                    return Response({
                        "records": 1,
                        "code": 200,
                        "message": "Login exitoso, se genero un nuevo token",
                        "results": [{
                            'token' : gToken,
                            'mail' : oUser.mail,
                            'user_type' : oUser.user_type.id
                        }]
                    })
            else : 
                return Response({
                    "records": 0,
                    "code": 500,
                    "message": "usuario/password incorrecta",
                    "results": []
                })
        except user.DoesNotExist:
            return Response({
                "records": 0,
                "code": 500,
                "message": "usuario/password incorrecta",
                "results": []
            })

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class countryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess | IsAuthenticated]
    queryset = country.objects.all()
    serializer_class = countrySerializer


class userViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess | IsAuthenticated]
    queryset = user.objects.all()
    serializer_class = userSerializer
    def create(self, request):
        request.data._mutable = True
        request.data['password']  = hashlib.md5(request.data['password'].encode()).hexdigest()
        request.data._mutable = False
        serializer = userSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class supplierViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess | IsAuthenticated]
    queryset = supplier.objects.all()
    serializer_class = supplierSerializer

class productCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess | IsAuthenticated]
    queryset = product_category.objects.all()
    serializer_class = productCategorySerializer

class productViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess | IsAuthenticated]
    queryset = product.objects.all()
    serializer_class = productSerializer


class customerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess | IsAuthenticated]
    queryset = customer.objects.all()
    serializer_class = customerSerializer


class paymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess | IsAuthenticated]
    queryset = payment.objects.all()
    serializer_class = paymentSerializer

class rezViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess | IsAuthenticated]
    queryset = rez.objects.all()
    serializer_class = rezSerializer


class auditViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess | IsAuthenticated]
    queryset = audit.objects.all()
    serializer_class = auditSerializer

