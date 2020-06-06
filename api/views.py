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
    permission_classes = [checkAccess]
    queryset = user_type.objects.all()
    serializer_class = userTypeSerializer
    
    def create(self, request):
        if canCreate(request,'userType') == True :
            serializer = userTypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized"})  

    def update(self, request, pk=None):
        if canCreate(request,'userType') == True :
            serializer = userTypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized"})  

    def list(self, request):
        queryset = user_type.objects.all()
        serializer = userTypeSerializer(queryset, many=True)
        return Response(serializer.data)




class getProfileView(APIView):
    permission_classes = [checkAccess]
    queryset = user.objects.all()
    serializer_class = getUserSerializer

    def get(self, request):
        try:
            userMail = request.headers['mail']
            queryset = user.objects.filter(mail = userMail)
            serializer = getUserSerializer(queryset, many=True)
            return Response(serializer.data)
        except:
            return Response({"code": 403, "message": "Not Authorized"})

    def put(self, request, pk, format=None):
        userGet = self.get_object(pk)
        request.data._mutable = True
        fMail = request.data['mail']
        oUser = user.objects.get(mail = fMail)
        request.data['password'] = oUser.password
        request.data._mutable = False
        serializerform = userSerializer(data=request.data)        
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = fMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                if (obj.user.user_type.description == 'Admin' or obj.user.mail == fMail):
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    return Response(serializer.errors)               
                else:
                    return Response({"code": 403, "message": "Not Authorized"}) 
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized"})  


class updatePasswordView(APIView):
    permission_classes = [checkAccess]
    queryset = user.objects.all()
    serializer_class = userSerializer

    def put(self, request, pk=None, format=None):
        request.data._mutable = True
        fMail = request.data['mail']
        fPassword = request.data['password']
        ePassword = hashlib.md5(fPassword.encode()).hexdigest()
        request.data['password'] = ePassword
        request.data._mutable = False
        userToUpdate = get_object_or_404(user.objects.all(), id=request.data['id'])
        serializer = userSerializer(instance=userToUpdate,data=request.data,partial=True)        
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                if (obj.user.user_type.description == 'Admin' or obj.user.mail == fMail):
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    return Response(serializer.errors)               
                else:
                    return Response({"code": 403, "message": "Not Authorized"}) 
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized"})  

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
                                'token' : obj.token,
                                'mail' : oUser.mail,
                                'fullname' : oUser.name + ' ' + oUser.lastname,
                                'user_type' : oUser.user_type.id
                            })               
                except token.DoesNotExist:
                    kToken = oUser.mail + oUser.password + str(today)
                    gToken = hashlib.md5(kToken.encode()).hexdigest()
                    cToken = token(date = today , user = oUser, token = gToken)
                    cToken.save()
                    return Response({
                            'token' : gToken,
                            'mail' : oUser.mail,
                            'fullname' : oUser.name + ' ' + oUser.lastname,
                            'user_type' : oUser.user_type.id
                        })
            else : 
                return Response({"code": 403, "message": "Not Authorized"})  
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized"})  


class countryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess]
    queryset = country.objects.all()
    serializer_class = countrySerializer
    def list(self, request):
        queryset = country.objects.all()
        serializer = countrySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        if canCreate(request,'country') == True :
            serializer = countrySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized"})  

    def update(self, request, pk=None):
        if canCreate(request,'country') == True :
            serializer = countrySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized"})  

class userViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess]
    queryset = user.objects.all()
    serializer_class = userSerializer


    def create(self, request):
        if canCreate(request,'user') == True :
            request.data._mutable = True
            request.data['password']  = hashlib.md5(request.data['password'].encode()).hexdigest()
            request.data._mutable = False            
            serializer = userSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized"})  

    def list(self, request):
        queryset = user.objects.all()
        serializer = getUserSerializer(queryset, many=True)
        return Response(serializer.data)


    def update(self, request, pk=None):
        if canCreate(request,'user') == True :
            request.data._mutable = True
            request.data['password']  = hashlib.md5(request.data['password'].encode()).hexdigest()
            request.data._mutable = False            
            serializer = userSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized"})  

class supplierViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess]
    queryset = supplier.objects.all()
    serializer_class = supplierSerializer
    def list(self, request):
        queryset = supplier.objects.all()
        serializer = supplierSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        if canCreate(request,'supplier') == True :
            serializer = supplierSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized"})  

    def update(self, request, pk=None):
        if canCreate(request,'supplier') == True :
            serializer = supplierSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized"})  
 

class productCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess]
    queryset = product_category.objects.all()
    serializer_class = productCategorySerializer
    def list(self, request):
        queryset = product_category.objects.all()
        serializer = productCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        if canCreate(request,'productCategory') == True :
            serializer = productCategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized"})  

    def update(self, request, pk=None):
        if canCreate(request,'productCategory') == True :
            serializer = productCategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized"})  

class productViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess]
    queryset = product.objects.all()
    serializer_class = productSerializer
    def list(self, request):
        queryset = product.objects.all()
        serializer = productSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        if canCreate(request,'product') == True :
            serializer = productSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized"})  

    def update(self, request, pk=None):
        if canCreate(request,'product') == True :
            serializer = productSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized"})  

class customerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess]
    queryset = customer.objects.all()
    serializer_class = customerSerializer
    def list(self, request):
        queryset = customer.objects.all()
        serializer = customerSerializer(queryset, many=True)
        return Response(serializer.data)
 
    def create(self, request):
        serializer = customerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class paymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess]
    queryset = payment.objects.all()
    serializer_class = paymentSerializer
    def list(self, request):
        queryset = payment.objects.all()
        serializer = paymentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = paymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class rezViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess]
    queryset = rez.objects.all()
    serializer_class = rezSerializer

    def list(self, request):
        try:
            userMail = request.headers['mail']
            try:
                oUser = user.objects.get(mail = userMail)
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                    queryset = rez.objects.all()
                elif (oUser.user_type.description == 'Employee'):
                    queryset = rez.objects.filter(user = oUser.id)
                serializer = rezSerializer(queryset, many=True)
                return Response(serializer.data)                
            except user.DoesNotExist:
                return Response({"code": 403, "message": "Not Authorized"})    
        except:
               return Response({"code": 403, "message": "Not Authorized"})    

    def create(self, request):
        serializer = rezSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class auditViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess]
    queryset = audit.objects.all()
    serializer_class = auditSerializer
    def list(self, request):
        if checkAccess(request,'audit','get') == 'OK':
            queryset = audit.objects.all()
            serializer = auditSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"status_code": 403, "detail": "Not Authorized"})  



def canCreate(request,endpoint):
    try:
        userMail = request.headers['mail']
        try:
            oUser = user.objects.get(mail = userMail)
            try:
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                    return True
                elif (oUser.user_type.description == 'Employee'):
                    return False
                else:
                    return False
            except token.DoesNotExist:
                return False
        except user.DoesNotExist:
            return False
    except:
        return False 
 