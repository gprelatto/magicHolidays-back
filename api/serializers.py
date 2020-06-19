from .models import *
from rest_framework import serializers


class userTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user_type
        fields = ['id','description']

class countrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = country
        fields = ['id','description','lang']

class userSerializer(serializers.HyperlinkedModelSerializer):
    user_type = serializers.PrimaryKeyRelatedField(queryset=user_type.objects.all(), many=False)
    country = serializers.PrimaryKeyRelatedField(queryset=country.objects.all(), many=False)
    class Meta:
        model = user
        fields = ['id','user_type','country','password','name','lastname','mail','phone']
 
class getUserSerializer(serializers.HyperlinkedModelSerializer):
    user_type = serializers.PrimaryKeyRelatedField(queryset=user_type.objects.all(), many=False)
    country = serializers.PrimaryKeyRelatedField(queryset=country.objects.all(), many=False)
    class Meta:
        model = user
        fields = ['id','user_type','country','name','lastname','mail','phone']


class loginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = user
        fields = ['mail','password']

class supplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = supplier
        fields = ['id','description']

class productCategorySerializer(serializers.HyperlinkedModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=supplier.objects.all(), many=False)
    class Meta:
        model = product_category
        fields = ['id','supplier','description']

class productSerializer(serializers.HyperlinkedModelSerializer):
    product_category = serializers.PrimaryKeyRelatedField(queryset=product_category.objects.all(), many=False)
    class Meta:
        model = product
        fields = ['id','product_category','description']

class customerSerializer(serializers.HyperlinkedModelSerializer):
    country = serializers.PrimaryKeyRelatedField(queryset=country.objects.all(), many=False)
    created_by = serializers.PrimaryKeyRelatedField(queryset=customer.objects.all(), many=False)
    class Meta:
        model = customer
        fields = ['id','fullname','mail','phone','country','created_by']

class paymentSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = payment
        fields = ['id','rez','prepaidDate','payDate','cancelationDate','transactionNumber']


class paymentPostSerializer(serializers.HyperlinkedModelSerializer):
    rez = serializers.PrimaryKeyRelatedField(queryset=rez.objects.all(), many=False)
    class Meta:
        model = payment
        fields = ['id','rez','prepaidDate','payDate','cancelationDate','transactionNumber']

class prepaidSerializer(serializers.HyperlinkedModelSerializer):
    prepaidDate = serializers.CharField(required=False,allow_blank=True)
    class Meta:
        depth = 1
        model = payment
        fields = ['id','reservations','prepaidDate']


class paySerializer(serializers.HyperlinkedModelSerializer):
    reservations = serializers.StringRelatedField(many=True)
    prepayDate = serializers.CharField(required=False,allow_blank=True)
    payDate = serializers.CharField(required=False,allow_blank=True)
    transactionNumber = serializers.CharField(required=False,allow_blank=True)
    class Meta:
        model = payment
        fields = ['id','reservations','prepaidDate','payDate','transactionNumber']


class cancelSerializer(serializers.HyperlinkedModelSerializer):
    reservations = serializers.StringRelatedField(many=True)
    cancelationDate = serializers.CharField(required=False,allow_blank=True)
    class Meta:
        model = payment
        fields = ['id','reservations','cancelationDate']

class rezPrepaySerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=product.objects.all(), many=False)
    customer = serializers.PrimaryKeyRelatedField(queryset=customer.objects.all(), many=False)
    user = serializers.PrimaryKeyRelatedField(queryset=user.objects.all(), many=False, required=False)
    class Meta:
        model = rez
        fields = ['id','product','customer','user','confirmationNumber','confirmationDate','arrivalDate','total','feeTotal','feeAgency','feeUser']
        depth = 1        

class rezSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=product.objects.all(), many=False)
    customer = serializers.PrimaryKeyRelatedField(queryset=customer.objects.all(), many=False)
    user = serializers.PrimaryKeyRelatedField(queryset=user.objects.all(), many=False, required=False)
    confirmationNumber = serializers.CharField(required=False,allow_blank=True)
    class Meta:
        model = rez
        fields = ['id','product','customer','user','confirmationNumber','confirmationDate','arrivalDate','total','feeTotal','feeAgency','feeUser','deleted_at']

class auditSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=user.objects.all(), many=False)
    class Meta:
        model = audit
        fields = ['id','description','user']