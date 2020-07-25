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
from django.http import JsonResponse
from rest_framework.views import APIView
from datetime import date
from django.shortcuts import get_object_or_404
from django.db import connection

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
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

    def update(self, request, pk=None):
        if canCreate(request,'userType') == True :
            obj_to_edit = user_type.objects.get(id = request.data["id"])
            serializer = userTypeSerializer(obj_to_edit, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

    def list(self, request):
        queryset = user_type.objects.all()
        serializer = userTypeSerializer(queryset, many=True)
        return Response(serializer.data)

class notificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess]
    queryset = notification.objects.all()
    serializer_class = notificationSerializer
    
    def create(self, request):
        if canCreate(request,'userType') == True :
            serializer = notificationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

    def update(self, request, pk=None):
        if canCreate(request,'userType') == True :
            obj_to_edit = notification.objects.get(id = request.data["id"])
            serializer = notificationSerializer(obj_to_edit, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

    def list(self, request):
        queryset = notification.objects.all()
        serializer = notificationSerializer(queryset, many=True)
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
            return Response({"code": 403, "message": "Not Authorized", "data" : []})

    def post(self, request, *args, **kwargs):
        obj_to_edit = user.objects.get(id = request.data["id"])
        request.data['password'] = obj_to_edit.password
        fMail = obj_to_edit.mail
        serializer = userSerializer(obj_to_edit, data=request.data)        
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
                    return Response({"code": 403, "message": "Not Authorized", "data" : []})
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 


class updatePasswordView(APIView):
    permission_classes = [checkAccess]
    queryset = user.objects.all()
    serializer_class = userSerializer

    def post(self, request, *args, **kwargs):
        try:
            
            userMail = request.headers['mail']
            userToken = request.headers['token']   
            fPassword = request.data['password']    
            oUser = user.objects.get(mail = userMail)
            userEdited = {
                'id' : oUser.id,
                'user_type' : oUser.user_type.id,
                'country' : oUser.country.id,
                'password' : hashlib.md5(request.data['password'].encode()).hexdigest(),
                'name'  : oUser.name,
                'lastname' : oUser.lastname,
                'mail' : oUser.mail
            }
            serializer = userSerializer(oUser,data=userEdited)        
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                if (obj.user.user_type.description == 'Admin' or obj.user.mail == userMail):
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    return Response(serializer.errors)               
                else:
                    return Response({"code": 403, "message": "Not Authorized", "data" : []})
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

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
                                'user_type' : oUser.user_type.id,
                                'lang' : oUser.country.lang,
                                'feePercentage' : oUser.user_type.feePercentage
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
                            'user_type' : oUser.user_type.id,
                            'lang' : oUser.country.lang,
                            'feePercentage' : oUser.user_type.feePercentage
                        })
            else : 
                return Response({"code": 403, "message": "Not Authorized", "data" : []}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 


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
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

    def update(self, request, pk=None):
        if canCreate(request,'country') == True :
            obj_to_edit = country.objects.get(id = request.data["id"])
            serializer = countrySerializer(obj_to_edit, data=request.data)                    
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

class userViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess]
    queryset = user.objects.all()
    serializer_class = userSerializer


    def create(self, request):
        if canCreate(request,'user') == True :
            try:
                oUserExists = user.objects.get(mail = request.data["mail"])
                return Response({"code": 500, "message": "User Exists!"}) 
            except user.DoesNotExist:
                request.data._mutable = True
                request.data['password']  = hashlib.md5(request.data['password'].encode()).hexdigest()
                request.data._mutable = False     
                serializer = userSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

    def list(self, request):
        queryset = user.objects.all()
        serializer = getUserSerializer(queryset, many=True)
        return Response(serializer.data)


    def update(self, request, pk=None):
        if canCreate(request,'user') == True :
            obj_to_edit = user.objects.get(id = request.data["id"])
            if (request.data['password'] == ''):
                request.data._mutable = True
                request.data['password']  = obj_to_edit.password
                request.data._mutable = False
            else:
                request.data._mutable = True
                request.data['password']  = hashlib.md5(request.data['password'].encode()).hexdigest()
                request.data._mutable = False   
            serializer = userSerializer(obj_to_edit, data=request.data)                                         
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

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
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

    def update(self, request, pk=None):
        if canCreate(request,'supplier') == True :
            obj_to_edit = supplier.objects.get(id = request.data["id"])
            serializer = supplierSerializer(obj_to_edit, data=request.data)              
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 
 

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
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

    def update(self, request, pk=None):
        if canCreate(request,'productCategory') == True :
            obj_to_edit = product_category.objects.get(id = request.data["id"])
            serializer = productCategorySerializer(obj_to_edit, data=request.data)                          
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

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
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

    def update(self, request, pk=None):
        if canCreate(request,'product') == True :
            obj_to_edit = product.objects.get(id = request.data["id"])
            serializer = productSerializer(obj_to_edit, data=request.data)                                      
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

class customerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess]
    queryset = customer.objects.all()
    serializer_class = customerSerializer

    def list(self, request):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                    queryset = customer.objects.all()
                else:
                    queryset = customer.objects.filter(created_by = oUser.id)
                serializer = customerSerializer(queryset, many=True)
                return Response(serializer.data)    
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 
 
    def create(self, request):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                request.data['created_by'] = oUser.id
                serializer = customerSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors)
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 



    def update(self, request, pk=None):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                request.data['created_by'] = oUser.id
                obj_to_edit = customer.objects.get(id = request.data["id"])
                serializer = customerSerializer(obj_to_edit, data=request.data)  
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors)
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

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


class prepaidViewSet(APIView):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess]
    queryset = payment.objects.all()
    serializer_class = prepaidSerializer

    def get(self, request):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                if (obj.user.user_type.description == 'Admin'):
                    queryset = rez.objects.filter(rel_payment_rez__isnull = True)
                    serializer = rezPrepaySerializer(queryset, many=True)
                    return Response(serializer.data)             
                else:
                    return Response({"code": 403, "message": "Not Authorized", "data" : []})
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

    def post(self, request, *args, **kwargs):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                if (obj.user.user_type.description == 'Admin'):
                    errorData = ''
                    errorFlag = 0
                    for i in request.data['reservations']:
                        obj_to_put = {
                            "id" : 0,
                            "rez" :  i  ,
                            'prepaidDate' : request.data['prepaidDate'],
                            'payDate' : None,
                            'cancelationDate' : None,
                            'transactionNumber' : None
                        }
                        serializer = paymentPostSerializer(data=obj_to_put)    
                        if serializer.is_valid():
                            serializer.save()
                        else :
                            errorFlag = errorFlag + 1
                            errorData = errorData + 'Reservation : ' + str(i) + ', Error: ' + str(errorData) + ' .'
                    if errorFlag > 0 :
                        return Response({"code": 500, "message": errorData})
                    else :
                        return Response({"code": 200, "message": "All payments succesfully generated"})
                else:
                    return Response({"code": 403, "message": "Not Authorized", "data" : []})
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 


class payDeleteViewSet(APIView):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess]
    queryset = payment.objects.all()
    serializer_class = prepaidSerializer

    def delete(self, request, pk, format=None):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                if (obj.user.user_type.description == 'Admin'):
                    obj_to_edit = payment.objects.get(pk=pk)
                    obj_to_put = {
                        "id" : obj_to_edit.id,
                        "rez" : obj_to_edit.rez,
                        'prepaidDate' : obj_to_edit.prepaidDate,
                        'payDate' : obj_to_edit.payDate,
                        'cancelationDate' : today,
                        'transactionNumber' : obj_to_edit.transactionNumber
                    }
                    serializer = paymentSerializer(obj_to_edit, data=obj_to_put)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response({"code": 500, "message": serializer.errorData}) 
                    return Response({"code": 200, "message": serializer.data})
                else:
                    return Response({"code": 403, "message": "Not Authorized", "data" : []})
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

class payViewSet(APIView):
    """
    API endpoint that allows taxes to be viewed or edited.
    """
    permission_classes = [checkAccess]
    queryset = payment.objects.all()
    serializer_class = prepaidSerializer

    def get(self, request):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                if (obj.user.user_type.description == 'Admin'):
                    queryset = payment.objects.filter(prepaidDate__isnull=False).filter(payDate__isnull=True)
                    serializer = paymentSerializer(queryset, many=True)
                    return Response(serializer.data)             
                else:
                    return Response({"code": 403, "message": "Not Authorized", "data" : []})
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

    def post(self, request, *args, **kwargs):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                if (obj.user.user_type.description == 'Admin'):
                    errorData = ''
                    errorFlag = 0
                    for i in request.data['reservations']:
                        obj_to_edit = payment.objects.get(rez=i)
                        obj_to_put = {
                            "id" : obj_to_edit.id,
                            "rez" : i,
                            'prepaidDate' : obj_to_edit.prepaidDate,
                            'payDate' : request.data['payDate'],
                            'cancelationDate' : None,
                            'transactionNumber' : request.data['transactionNumber']
                        }
                        serializer = paymentPostSerializer(obj_to_edit, data=obj_to_put)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            errorFlag = errorFlag + 1
                            errorData = errorData + 'Reservation : ' + str(i) + ', Error: ' + str(errorData) + ' .'
                    if errorFlag > 0 :
                        return Response({"code": 500, "message": errorData})
                    else :
                        return Response({"code": 200, "message": "All payments succesfully generated"})
                else:
                    return Response({"code": 403, "message": "Not Authorized", "data" : []})
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 


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
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                    queryset = rez.objects.all()
                else:
                    queryset = rez.objects.filter(user = oUser.id)
                serializer = rezSerializer(queryset, many=True)
                return Response(serializer.data)    
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

    def create(self, request):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                request.data['user'] = oUser.id
                serializer = rezSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors)
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []})         

    def update(self, request, pk=None):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                if request.data['user'] == oUser.id or oUser.user_type.description == 'Admin':
                    obj_to_edit = rez.objects.get(id = request.data["id"])
                    serializer = rezSerializer(obj_to_edit, data=request.data)                                      
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    return Response(serializer.errors)                    
                else:
                    return Response({"code": 500, "message": "You dont own that reservation"})
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []})   

    def destroy(self, request, pk=None):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            oRez = rez.objects.get(id = pk)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                if oRez.user.id == oUser.id or oUser.user_type.description == 'Admin':
                    obj_to_edit = rez.objects.get(id = pk)
                    obj_edited = obj_to_edit
                    obj_edited.deleted_at = today
                    self.object = self.get_object()
                    self.object.soft_delete()               
                    return Response({"code": 200, "message": "Reservation cancelled"})     
                    # serializer = rezSerializer(obj_to_edit, data=serializers.serialize('json', [ obj_edited ]))                                      
                    # if serializer.is_valid():
                    #     serializer.save()
                    #     return Response(serializer.data)
                    #return Response(serializer.errors)                    
                else:
                    return Response({"code": 500, "message": "You dont own that reservation"})
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []})   


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


class getTotals(APIView):
    permission_classes = [checkAccess]
    queryset = rez.objects.all()

    def get(self, request):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                cursor = connection.cursor()
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                    cursor.execute('\
                        select \
                            u.name, \
                            u.lastname, \
                            sum(total) TotalSales, \
                            sum(r."feeTotal") as TotalFees, \
                            sum(r."feeAgency") as TotalFeeAgency, \
                            sum(r."feeUser") as TotalFeeUser,\
                            sum(case when py."prepaidDate" is not null and py."payDate" is null and py."cancelationDate" is null then r."feeUser" else 0 end) as TotalToPay,\
                            sum(case when py."prepaidDate" is not null and py."payDate" is not null and py."cancelationDate" is null then r."feeUser" else 0 end) as TotalPaid,\
                            sum(case when py."prepaidDate" is null and py."payDate" is null and py."cancelationDate" is null then r."feeTotal" else 0 end) as TotalToCollect,\
                            sum(case when py."cancelationDate" is not null then r."feeTotal" else 0 end) as TotalCancelled\
                        from api_rez r\
                        join api_user u on r.user_id = u.id \
                        join api_customer c on r.customer_id = c.id \
                        join api_product p on p.id = r.product_id \
                        join api_product_category pc on pc.id = p.product_category_id \
                        join api_supplier s on s.id = pc.supplier_id \
                        left join api_payment py on py.rez_id = r.id \
                        group by 1,2                  \
                    ')
                else:
                    command = """\
                        select \
                            u.name, \
                            u.lastname, \
                            sum(total) TotalSales, \
                            sum(r."feeTotal") as TotalFees, \
                            sum(r."feeAgency") as TotalFeeAgency, \
                            sum(r."feeUser") as TotalFeeUser,\
                            sum(case when py."prepaidDate" is not null and py."payDate" is null and py."cancelationDate" is null then r."feeUser" else 0 end) as TotalToPay,\
                            sum(case when py."prepaidDate" is not null and py."payDate" is not null and py."cancelationDate" is null then r."feeUser" else 0 end) as TotalPaid,\
                            sum(case when py."prepaidDate" is null and py."payDate" is null and py."cancelationDate" is null then r."feeTotal" else 0 end) as TotalToCollect,\
                            sum(case when py."cancelationDate" is not null then r."feeTotal" else 0 end) as TotalCancelled\
                        from api_rez r\
                        join api_user u on r.user_id = u.id \
                        join api_customer c on r.customer_id = c.id \
                        join api_product p on p.id = r.product_id \
                        join api_product_category pc on pc.id = p.product_category_id \
                        join api_supplier s on s.id = pc.supplier_id \
                        left join api_payment py on py.rez_id = r.id \
                        where r.user_id = {0} \
                        group by 1,2                 \
                    """.format(oUser.id)
                    cursor.execute(command)
                if cursor.rowcount > 0:
                    return Response(dictfetchall(cursor))    
                else:
                    return Response({"code": 200, "message": "No Data To Display", "data" : []}) 
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 


class getMonthlyTotals(APIView):
    permission_classes = [checkAccess]
    queryset = rez.objects.all()

    def get(self, request):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                cursor = connection.cursor()
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                   cursor.execute('\
                        select \
                            EXTRACT(YEAR from r."confirmationDate") as Year,\
                            EXTRACT(MONTH from r."confirmationDate") as Month,\
                            sum(r.total) TotalSales, \
                            sum(r."feeTotal") as TotalFees, \
                            sum(r."feeAgency") as TotalFeeAgency, \
                            sum(r."feeUser") as TotalFeeUser,\
                            sum(case when py."prepaidDate" is not null and py."payDate" is null and py."cancelationDate" is null then r."feeUser" else 0 end) as TotalToPay,\
                            sum(case when py."prepaidDate" is not null and py."payDate" is not null and py."cancelationDate" is null then r."feeUser" else 0 end) as TotalPaid,\
                            sum(case when py."prepaidDate" is null and py."payDate" is null and py."cancelationDate" is null then r."feeTotal" else 0 end) as TotalToCollect,\
                            sum(case when py."cancelationDate" is not null then r."feeTotal" else 0 end) as TotalCancelled\
                        from api_rez r\
                        join api_user u on r.user_id = u.id \
                        join api_customer c on r.customer_id = c.id \
                        join api_product p on p.id = r.product_id \
                        join api_product_category pc on pc.id = p.product_category_id \
                        join api_supplier s on s.id = pc.supplier_id \
                        left join api_payment py on py.rez_id = r.id \
                        group by 1,2\
                        order by 1,2\
                    ')
                else:
                    command = """\
                        select \
                            EXTRACT(YEAR from r."confirmationDate") as Year,\
                            EXTRACT(MONTH from r."confirmationDate") as Month,\
                            sum(r.total) TotalSales, \
                            sum(r."feeTotal") as TotalFees, \
                            sum(r."feeAgency") as TotalFeeAgency, \
                            sum(r."feeUser") as TotalFeeUser,\
                            sum(case when py."prepaidDate" is not null and py."payDate" is null and py."cancelationDate" is null then r."feeUser" else 0 end) as TotalToPay,\
                            sum(case when py."prepaidDate" is not null and py."payDate" is not null and py."cancelationDate" is null then r."feeUser" else 0 end) as TotalPaid,\
                            sum(case when py."prepaidDate" is null and py."payDate" is null and py."cancelationDate" is null then r."feeTotal" else 0 end) as TotalToCollect,\
                            sum(case when py."cancelationDate" is not null then r."feeTotal" else 0 end) as TotalCancelled\
                        from api_rez r\
                        join api_user u on r.user_id = u.id \
                        join api_customer c on r.customer_id = c.id \
                        join api_product p on p.id = r.product_id \
                        join api_product_category pc on pc.id = p.product_category_id \
                        join api_supplier s on s.id = pc.supplier_id \
                        left join api_payment py on py.rez_id = r.id \
                        where r.user_id = {0} \
                        group by 1,2\
                        order by 1,2\
                    """.format(oUser.id)
                    cursor.execute(command)
                if cursor.rowcount > 0:
                    return Response(dictfetchall(cursor))    
                else:
                    return Response({"code": 200, "message": "No Data To Display", "data" : []}) 
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 


class salesByProduct(APIView):
    permission_classes = [checkAccess]
    queryset = rez.objects.all()

    def get(self, request):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                cursor = connection.cursor()
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                    cursor.execute('\
                        select \
                            p.description as key,\
                            count(*) TotalSales\
                        from api_rez r\
                        join api_user u on r.user_id = u.id \
                        join api_customer c on r.customer_id = c.id \
                        join api_product p on p.id = r.product_id \
                        join api_product_category pc on pc.id = p.product_category_id \
                        join api_supplier s on s.id = pc.supplier_id \
                        left join api_payment py on py.rez_id = r.id \
                        group by 1\
                        order by 1\
                    ')
                else:
                    command = """\
                        select \
                            p.description as key,\
                            count(*) TotalSales\
                        from api_rez r\
                        join api_user u on r.user_id = u.id \
                        join api_customer c on r.customer_id = c.id \
                        join api_product p on p.id = r.product_id \
                        join api_product_category pc on pc.id = p.product_category_id \
                        join api_supplier s on s.id = pc.supplier_id \
                        left join api_payment py on py.rez_id = r.id \
                        where r.user_id = {0} \
                        group by 1\
                        order by 1\
                    """.format(oUser.id)
                    cursor.execute(command)
                if cursor.rowcount > 0:
                    return Response(dictfetchall(cursor))    
                else:
                    return Response({"code": 200, "message": "No Data To Display", "data" : []}) 
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

class salesByCountry(APIView):
    permission_classes = [checkAccess]
    queryset = rez.objects.all()

    def get(self, request):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                cursor = connection.cursor()
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                    cursor.execute('select * from vw_sales_country')
                else:
                   return Response({"code": 403, "message": "Not Authorized"})
                if cursor.rowcount > 0:
                    return Response(dictfetchall(cursor))    
                else:
                    return Response({"code": 200, "message": "No Data To Display", "data" : []}) 
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 


class widgetsData(APIView):
    permission_classes = [checkAccess]
    queryset = rez.objects.all()

    def get(self, request):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                cursor = connection.cursor()
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                    command = """select * from vw_widgets_admin"""
                    cursor.execute(command)
                else:
                    command = """select * from vw_widgets_employee where id = {0}""".format(oUser.id)
                    cursor.execute(command)
                if cursor.rowcount > 0:
                    return Response(dictfetchall(cursor))
                else:
                    return Response({"code": 200, "message": "No Data To Display", "data" : []}) 
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

class salesByProvider(APIView):
    permission_classes = [checkAccess]
    queryset = rez.objects.all()

    def get(self, request):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                cursor = connection.cursor()
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                    command = """\
                        select * from vw_providerSales_admin
                    """
                    cursor.execute(command)
                else:
                    command = """\
                        select * from vw_providerSales_employee where id = {0}
                    """.format(oUser.id)
                    cursor.execute(command)
                if cursor.rowcount > 0:
                    return Response(dictfetchall(cursor))
                else:
                    return Response({"code": 200, "message": "No Data To Display", "data" : []}) 
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 


class salesByEmployee(APIView):
    permission_classes = [checkAccess]
    queryset = rez.objects.all()

    def get(self, request):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                cursor = connection.cursor()
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                    command = """\
                        select * from vw_sales_employee
                    """
                    cursor.execute(command)
                else:
                    return Response({"code": 403, "message": "Not Authorized", "data" : []}) 
                if cursor.rowcount > 0:
                    return Response(dictfetchall(cursor))
                else:
                    return Response({"code": 200, "message": "No Data To Display", "data" : []}) 
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

class detailedSales(APIView):
    permission_classes = [checkAccess]
    queryset = rez.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                cursor = connection.cursor()
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                    command = """\
                        select \
                            u.name, \
                            u.lastname,\
                            r."confirmationDate" ,\
                            r."arrivalDate",\
                            r."confirmationNumber",\
                            s.description as Supplier,\
                            pc.description as Category,\
                            p.description as Product,\
                            total, \
                            r."feeTotal" as TotalFees, \
                            r."feeAgency" as TotalFeeAgency, \
                            r."feeUser" as TotalFeeUser,\
                            case when py."prepaidDate" is not null and py."payDate" is null and py."cancelationDate" is null then r."feeUser" else 0 end as TotalToPay,\
                            case when py."prepaidDate" is not null and py."payDate" is not null and py."cancelationDate" is null then r."feeUser" else 0 end as TotalPaid,\
                            case when py."prepaidDate" is null and py."payDate" is null and py."cancelationDate" is null then r."feeTotal" else 0 end as TotalToCollect,\
                            case when py."cancelationDate" is not null then r."feeTotal" else 0 end as TotalCancelled,\
                            py."transactionNumber" \
                        from api_rez r\
                        join api_user u on r.user_id = u.id \
                        join api_customer c on r.customer_id = c.id \
                        join api_product p on p.id = r.product_id \
                        join api_product_category pc on pc.id = p.product_category_id \
                        join api_supplier s on s.id = pc.supplier_id \
                        left join api_payment py on py.rez_id = r.id \
                        join api_country cy on cy.id = c.country_id\
                        where r."confirmationDate" between '{0}' and '{1}'\
                    """.format(request.data['dateFrom'],request.data['dateTo'])
                    cursor.execute(command)
                    if cursor.rowcount > 0:
                        return Response(dictfetchall(cursor))    
                    else:
                        return Response({"code": 200, "message": "No Data To Display", "data" : []}) 
                else:
                    return Response({"code": 403, "message": "Not Authorized", "data" : []}) 
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 

class travelAlerts(APIView):
    permission_classes = [checkAccess]
    queryset = rez.objects.all()

    def get(self, request):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                cursor = connection.cursor()
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                    command = """\
                        SELECT * FROM vw_travel_alerts
                    """
                    cursor.execute(command)
                else:
                    command = """\
                        SELECT * FROM vw_travel_alerts WHERE user_id = {0}\
                    """.format(oUser.id)
                    cursor.execute(command)
                if cursor.rowcount > 0:
                    return Response(dictfetchall(cursor))    
                else:
                    return Response({"code": 200, "message": "No Data To Display", "data" : []}) 
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 



class toPay(APIView):
    permission_classes = [checkAccess]
    queryset = rez.objects.all()

    def get(self, request):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                cursor = connection.cursor()
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                    command = """\
                        SELECT \
                            c."id" ,\
                            c."name" ,\
                            c.lastname ,\
                            a."confirmationDate" ,\
                            g.fullname ,\
                            a."arrivalDate",\
                            f.description  as Supplier,\
                            e.description as Category,\
                            d.description as Product,\
                            a.total ,\
                            a."confirmationNumber" ,\
                            a."feeTotal" ,\
                            a."feeUser" \
                        FROM api_rez a\
                        LEFT JOIN api_payment b on a.id = b.rez_id \
                        join api_user c on a.user_id = c.id \
                        join api_product d on a.product_id = d.id \
                        join api_product_category e on d.product_category_id = e.id \
                        join api_supplier f on f.id = e.supplier_id\
                        join api_customer g on g.id = a.customer_id \
                        where b.id is null and a.deleted_at is null\
                    """
                    cursor.execute(command)
                else:
                    command = """\
                        SELECT \
                            c."id" ,\
                            c."name" ,\
                            c."lastname" ,\
                            a."confirmationDate" ,\
                            g.fullname ,\
                            a."arrivalDate",\
                            f.description  as Supplier,\
                            e.description as Category,\
                            d.description as Product,\
                            a.total ,\
                            a."confirmationNumber" ,\
                            a."feeTotal" ,\
                            a."feeUser" \
                        FROM api_rez a\
                        LEFT JOIN api_payment b on a.id = b.rez_id \
                        join api_user c on a.user_id = c.id \
                        join api_product d on a.product_id = d.id \
                        join api_product_category e on d.product_category_id = e.id \
                        join api_supplier f on f.id = e.supplier_id\
                        join api_customer g on g.id = a.customer_id \
                        where b.id is null and a.user_id = {0} and a.deleted_at is null\
                    """.format(oUser.id)
                    cursor.execute(command)
                if cursor.rowcount > 0:
                    return Response(dictfetchall(cursor))    
                else:
                    return Response({"code": 200, "message": "No Data To Display", "data" : []}) 
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 


class paid(APIView):
    permission_classes = [checkAccess]
    queryset = rez.objects.all()

    def get(self, request):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                cursor = connection.cursor()
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                    command = """\
                        SELECT \
                            c."id" ,\
                            c."name" ,\
                            c.lastname ,\
                            a."confirmationDate" ,\
                            g.fullname ,\
                            a."arrivalDate",\
                            f.description  as Supplier,\
                            e.description as Category,\
                            d.description as Product,\
                            a.total ,\
                            a."confirmationNumber" ,\
                            a."feeTotal" ,\
                            a."feeUser", \
                            b."payDate" , \
                            b."transactionNumber" \
                        FROM api_rez a\
                        JOIN api_payment b on a.id = b.rez_id \
                        join api_user c on a.user_id = c.id \
                        join api_product d on a.product_id = d.id \
                        join api_product_category e on d.product_category_id = e.id \
                        join api_supplier f on f.id = e.supplier_id\
                        join api_customer g on g.id = a.customer_id \
                        where b."payDate" is not null\
                    """
                    cursor.execute(command)
                else:
                    command = """\
                        SELECT \
                            c."id" ,\
                            c."name" ,\
                            c."lastname" ,\
                            a."confirmationDate" ,\
                            g.fullname ,\
                            a."arrivalDate",\
                            f.description  as Supplier,\
                            e.description as Category,\
                            d.description as Product,\
                            a.total ,\
                            a."confirmationNumber" ,\
                            a."feeTotal" ,\
                            a."feeUser", \
                            b."payDate" , \
                            b."transactionNumber" \
                        FROM api_rez a\
                        JOIN api_payment b on a.id = b.rez_id \
                        join api_user c on a.user_id = c.id \
                        join api_product d on a.product_id = d.id \
                        join api_product_category e on d.product_category_id = e.id \
                        join api_supplier f on f.id = e.supplier_id\
                        join api_customer g on g.id = a.customer_id \
                        where b."payDate" is not null and a.user_id = {0}\
                    """.format(oUser.id)
                    cursor.execute(command)
                if cursor.rowcount > 0:
                    return Response(dictfetchall(cursor))    
                else:
                    return Response({"code": 200, "message": "No Data To Display", "data" : []}) 
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized", "data" : []}) 




def canCreate(request,endpoint):
    try:
        userMail = request.headers['mail']
        try:
            oUser = user.objects.get(mail = userMail)
            try:
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                    return True
                else:
                    return False
            except token.DoesNotExist:
                return False
        except user.DoesNotExist:
            return False
    except:
        return False 
 

from collections import namedtuple

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
