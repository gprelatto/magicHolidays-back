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
                responseData = {
                    'code' : '200',
                    'message' : 'AUTHORIZED',
                    'data' : serializer.data
                }                
                return Response(responseData)
            responseData = {
                'code' : '500',
                'message' : 'ERRORS',
                'data' : serializer.errors
            }                
            return Response(responseData)
        else:
            responseData = {
                'code' : '403',
                'message' : 'UNAUTHORIZED',
                'data' : []
            }                     
            return Response(responseData)

    def list(self, request):
        queryset = user_type.objects.all()
        serializer = userTypeSerializer(queryset, many=True)
        responseData = {
            'code' : '200',
            'message' : 'AUTHORIZED',
            'data' : serializer.data
        }
        return Response(responseData)




class getProfileView(APIView):
    permission_classes = []
    queryset = user.objects.all()
    serializer_class = getUserSerializer

    def get(self, request):
        try:
            userMail = request.headers['mail']
            queryset = user.objects.filter(mail = userMail)
            serializer = getUserSerializer(queryset, many=True)
            responseData = {
                'code' : '200',
                'message' : 'AUTHORIZED',
                'data' : serializer.data
            }
            return Response(responseData)
        except:
            responseData = {
                'code' : '500',
                'message' : 'Problem on Request',
                'data' : []
            }
            return Response(responseData)



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
        responseData = {
            'code' : '200',
            'message' : 'AUTHORIZED',
            'data' : serializer.data
        }
        return Response(responseData)

    def create(self, request):
        if canCreate(request,'country') == True :
            serializer = countrySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                responseData = {
                    'code' : '200',
                    'message' : 'AUTHORIZED',
                    'data' : serializer.data
                }                
                return Response(responseData)
            responseData = {
                'code' : '500',
                'message' : 'ERRORS',
                'data' : serializer.errors
            }                
            return Response(responseData)
        else:
            responseData = {
                'code' : '403',
                'message' : 'UNAUTHORIZED',
                'data' : []
            }                     
            return Response(responseData)

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
                responseData = {
                    'code' : '200',
                    'message' : 'AUTHORIZED',
                    'data' : serializer.data
                }                
                return Response(responseData)
            responseData = {
                'code' : '500',
                'message' : 'ERRORS',
                'data' : serializer.errors
            }                
            return Response(responseData)
        else:
            responseData = {
                'code' : '403',
                'message' : 'UNAUTHORIZED',
                'data' : []
            }                     
            return Response(responseData)

    def list(self, request):
        queryset = user.objects.all()
        serializer = userSerializer(queryset, many=True)
        responseData = {
            'code' : '200',
            'message' : 'AUTHORIZED',
            'data' : serializer.data
        }
        return Response(responseData)



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
        responseData = {
            'code' : '200',
            'message' : 'AUTHORIZED',
            'data' : serializer.data
        }
        return Response(responseData)

    def create(self, request):
        if canCreate(request,'supplier') == True :
            serializer = supplierSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                responseData = {
                    'code' : '200',
                    'message' : 'AUTHORIZED',
                    'data' : serializer.data
                }                
                return Response(responseData)
            responseData = {
                'code' : '500',
                'message' : 'ERRORS',
                'data' : serializer.errors
            }                
            return Response(responseData)
        else:
            responseData = {
                'code' : '403',
                'message' : 'UNAUTHORIZED',
                'data' : []
            }                     
            return Response(responseData)

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
        responseData = {
            'code' : '200',
            'message' : 'AUTHORIZED',
            'data' : serializer.data
        }
        return Response(responseData)

    def create(self, request):
        if canCreate(request,'productCategory') == True :
            serializer = productCategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                responseData = {
                    'code' : '200',
                    'message' : 'AUTHORIZED',
                    'data' : serializer.data
                }                
                return Response(responseData)
            responseData = {
                'code' : '500',
                'message' : 'ERRORS',
                'data' : serializer.errors
            }                
            return Response(responseData)
        else:
            responseData = {
                'code' : '403',
                'message' : 'UNAUTHORIZED',
                'data' : []
            }                     
            return Response(responseData)

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
        responseData = {
            'code' : '200',
            'message' : 'AUTHORIZED',
            'data' : serializer.data
        }
        return Response(responseData)

    def create(self, request):
        if canCreate(request,'product') == True :
            serializer = productSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                responseData = {
                    'code' : '200',
                    'message' : 'AUTHORIZED',
                    'data' : serializer.data
                }                
                return Response(responseData)
            responseData = {
                'code' : '500',
                'message' : 'ERRORS',
                'data' : serializer.errors
            }                
            return Response(responseData)
        else:
            responseData = {
                'code' : '403',
                'message' : 'UNAUTHORIZED',
                'data' : []
            }                     
            return Response(responseData)

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
        responseData = {
            'code' : '200',
            'message' : 'AUTHORIZED',
            'data' : serializer.data
        }
        return Response(responseData)
 
    def create(self, request):
        serializer = customerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            responseData = {
                'code' : '200',
                'message' : 'AUTHORIZED',
                'data' : serializer.data
            }                
            return Response(responseData)
        responseData = {
            'code' : '500',
            'message' : 'ERRORS',
            'data' : serializer.errors
        }                
        return Response(responseData)

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
        responseData = {
            'code' : '200',
            'message' : 'AUTHORIZED',
            'data' : serializer.data
        }
        return Response(responseData)

    def create(self, request):
        serializer = paymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            responseData = {
                'code' : '200',
                'message' : 'AUTHORIZED',
                'data' : serializer.data
            }                
            return Response(responseData)
        responseData = {
            'code' : '500',
            'message' : 'ERRORS',
            'data' : serializer.errors
        }                
        return Response(responseData)

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
                responseData = {
                    'code' : '200',
                    'message' : 'AUTHORIZED',
                    'data' : serializer.data
                }
                return Response(responseData)                
            except user.DoesNotExist:
                responseData = {
                    'code' : '403',
                    'message' : 'USER NOT FOUND',
                    'data' : []
                }
                return Response(responseData)   
        except:
                responseData = {
                    'code' : '403',
                    'message' : 'HEADERS NOT FOUND',
                    'data' : []
                }
                return Response(responseData)   

    def create(self, request):
        serializer = rezSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            responseData = {
                'code' : '200',
                'message' : 'AUTHORIZED',
                'data' : serializer.data
            }                
            return Response(responseData)
        responseData = {
            'code' : '500',
            'message' : 'ERRORS',
            'data' : serializer.errors
        }                
        return Response(responseData)


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
            responseData = {
                'code' : '200',
                'message' : 'AUTHORIZED',
                'data' : serializer.data
            }
            return Response(responseData)
        else:
            responseData = {
                'code' : '403',
                'message' : 'NOT AUTHORIZED',
                'data' : []
            }           
            return Response(responseData)  



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
 