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
            request.data['password']  = hashlib.md5(request.data['password'].encode()).hexdigest()
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
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                if (oUser.user_type.description == 'Admin' or oUser.user_type.description == 'Owner'):
                    queryset = rez.objects.all()
                elif (oUser.user_type.description == 'Employee'):
                    queryset = rez.objects.filter(user = oUser.id)
                serializer = rezSerializer(queryset, many=True)
                return Response(serializer.data)    
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized"})  

    def create(self, request):
        try:
            userMail = request.headers['mail']
            userToken = request.headers['token']            
            oUser = user.objects.get(mail = userMail)
            today = date.today()
            try:
                obj = token.objects.get(user = oUser.id,date = today,token = userToken)
                request.data['user_id'] = oUser.id
                serializer = rezSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors)
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized"})          



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
                elif (oUser.user_type.description == 'Employee'):
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
                return Response(dictfetchall(cursor))
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized"})  


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
                elif (oUser.user_type.description == 'Employee'):
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
                return Response(dictfetchall(cursor))   
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized"})  


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
                elif (oUser.user_type.description == 'Employee'):
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
                return Response(dictfetchall(cursor))   
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized"})  

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
                    cursor.execute('\
                        select \
                            cy.description as key,\
                            count(*) TotalSales\
                        from api_rez r\
                        join api_user u on r.user_id = u.id \
                        join api_customer c on r.customer_id = c.id \
                        join api_product p on p.id = r.product_id \
                        join api_product_category pc on pc.id = p.product_category_id \
                        join api_supplier s on s.id = pc.supplier_id \
                        left join api_payment py on py.rez_id = r.id \
                        join api_country cy on cy.id = c.country_id \
                        group by 1\
                        order by 1\
                    ')
                elif (oUser.user_type.description == 'Employee'):
                    command = """\
                        select \
                            cy.description as key,\
                            count(*) TotalSales\
                        from api_rez r\
                        join api_user u on r.user_id = u.id \
                        join api_customer c on r.customer_id = c.id \
                        join api_product p on p.id = r.product_id \
                        join api_product_category pc on pc.id = p.product_category_id \
                        join api_supplier s on s.id = pc.supplier_id \
                        left join api_payment py on py.rez_id = r.id \
                        join api_country cy on cy.id = c.country_id \
                        where r.user_id = {0} \
                        group by 1\
                        order by 1\
                    """.format(oUser.id)
                    cursor.execute(command)
                return Response(dictfetchall(cursor))    
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized"})  


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
                    command = """\
                        select \
                            'Total Sales' as Widget,\
                            count(*) TotalSales\
                        from api_rez r\
                        join api_user u on r.user_id = u.id \
                        join api_customer c on r.customer_id = c.id \
                        join api_product p on p.id = r.product_id \
                        join api_product_category pc on pc.id = p.product_category_id \
                        join api_supplier s on s.id = pc.supplier_id \
                        join api_country cy on cy.id = c.country_id \
                        left join api_payment py on py.rez_id = r.id \
                        where cast( r."confirmationDate" as date) = cast (now() as date)\
                        union all \
                        select \
                            'Total Revenue' as Widget,\
                            SUM(r.total) TotalSales\
                        from api_rez r\
                        join api_user u on r.user_id = u.id \
                        join api_customer c on r.customer_id = c.id \
                        join api_product p on p.id = r.product_id \
                        join api_product_category pc on pc.id = p.product_category_id \
                        join api_supplier s on s.id = pc.supplier_id \
                        join api_country cy on cy.id = c.country_id \
                        left join api_payment py on py.rez_id = r.id \
                        where cast( r."confirmationDate" as date) = cast (now() as date)\
                        union all \
                        select \
                            'Total Fees' as Widget,\
                            SUM(r."feeUser") TotalSales\
                        from api_rez r\
                        join api_user u on r.user_id = u.id \
                        join api_customer c on r.customer_id = c.id \
                        join api_product p on p.id = r.product_id \
                        join api_product_category pc on pc.id = p.product_category_id \
                        join api_supplier s on s.id = pc.supplier_id \
                        join api_country cy on cy.id = c.country_id \
                        left join api_payment py on py.rez_id = r.id \
                        where cast( r."confirmationDate" as date) = cast (now() as date)\
                    """
                    cursor.execute(command)
                elif (oUser.user_type.description == 'Employee'):
                    command = """\
                        select \
                            'Total Sales' as Widget,\
                            count(*) TotalSales\
                        from api_rez r\
                        join api_user u on r.user_id = u.id \
                        join api_customer c on r.customer_id = c.id \
                        join api_product p on p.id = r.product_id \
                        join api_product_category pc on pc.id = p.product_category_id \
                        join api_supplier s on s.id = pc.supplier_id \
                        join api_country cy on cy.id = c.country_id \
                        left join api_payment py on py.rez_id = r.id \
                        where cast( r."confirmationDate" as date) = cast (now() as date) and r.user_id = {0} \
                        union all \
                        select \
                            'Total Revenue' as Widget,\
                            SUM(r.total) TotalSales\
                        from api_rez r\
                        join api_user u on r.user_id = u.id \
                        join api_customer c on r.customer_id = c.id \
                        join api_product p on p.id = r.product_id \
                        join api_product_category pc on pc.id = p.product_category_id \
                        join api_supplier s on s.id = pc.supplier_id \
                        join api_country cy on cy.id = c.country_id \
                        left join api_payment py on py.rez_id = r.id \
                        where cast( r."confirmationDate" as date) = cast (now() as date) and r.user_id = {0} \
                        union all \
                        select \
                            'Total Fees' as Widget,\
                            SUM(r."feeUser") TotalSales\
                        from api_rez r\
                        join api_user u on r.user_id = u.id \
                        join api_customer c on r.customer_id = c.id \
                        join api_product p on p.id = r.product_id \
                        join api_product_category pc on pc.id = p.product_category_id \
                        join api_supplier s on s.id = pc.supplier_id \
                        join api_country cy on cy.id = c.country_id \
                        left join api_payment py on py.rez_id = r.id \
                        where cast( r."confirmationDate" as date) = cast (now() as date) and r.user_id = {0} \
                    """.format(oUser.id)
                    cursor.execute(command)
                return Response(dictfetchall(cursor))    
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized"})  


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
                    return Response(dictfetchall(cursor))    
                else:
                    return Response({"code": 403, "message": "Not Authorized"})  
            except token.DoesNotExist:
                return Response({"code": 500, "message": "Invalid Token"}) 
        except user.DoesNotExist:
            return Response({"code": 403, "message": "Not Authorized"})  




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
 

from collections import namedtuple

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]