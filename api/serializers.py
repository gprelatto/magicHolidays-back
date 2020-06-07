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
    class Meta:
        model = customer
        fields = ['id','fullname','mail','phone','country']

class paymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = payment
        fields = ['id','prepaidDate','payDate','cancelationDate','transactionNumber']

class rezSerializer(serializers.HyperlinkedModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=product.objects.all(), many=False)
    customer = serializers.PrimaryKeyRelatedField(queryset=customer.objects.all(), many=False)
    user = serializers.PrimaryKeyRelatedField(queryset=user.objects.all(), many=False)
    class Meta:
        model = rez
        fields = ['id','product','customer','user','confirmationNumber','confirmationDate','arrivalDate','total','feeTotal','feeAgency','feeUser']

class auditSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=user.objects.all(), many=False)
    class Meta:
        model = audit
        fields = ['id','description','user']