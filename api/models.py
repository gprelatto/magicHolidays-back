from django.db import models
from django.contrib.auth.models import User


class notification(models.Model):
    date_from = models.DateTimeField(null=True)
    date_to = models.DateTimeField(null=True)
    message =  models.CharField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)    
    def __str__(self):
        return '%s' % (self.message)   

class user_type(models.Model):
    description =  models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)    
    def __str__(self):
        return '%s' % (self.description)   

class country(models.Model):
    description =  models.CharField(max_length=50)
    lang =  models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)    
    def __str__(self):
        return '%s' % (self.description)   

class user(models.Model):
    user_type =  models.ForeignKey(user_type, related_name='rel_user_userType', on_delete=models.PROTECT)
    country =  models.ForeignKey(country, related_name='rel_user_country', on_delete=models.PROTECT)
    password =  models.CharField(max_length=256)
    name =  models.CharField(max_length=60)
    lastname =  models.CharField(max_length=60)
    mail =  models.CharField(max_length=100)
    phone =  models.CharField(max_length=80,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)    
    def __str__(self):
        return '%s' % (self.mail)   

class supplier(models.Model):
    description =  models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)    
    def __str__(self):
        return '%s' % (self.description)   

class product_category(models.Model):
    supplier =  models.ForeignKey(supplier, related_name='rel_productCategory_supplier', on_delete=models.PROTECT)
    description =  models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)    
    def __str__(self):
        return '%s' % (self.description)   

class product(models.Model):
    product_category =  models.ForeignKey(product_category, related_name='rel_product_productCategory', on_delete=models.PROTECT)
    description =  models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)    
    def __str__(self):
        return '%s' % (self.description)   

class customer(models.Model):
    fullname =  models.CharField(max_length=150)
    mail =  models.CharField(max_length=100)
    phone =  models.CharField(max_length=80)
    country =  models.ForeignKey(country, related_name='rel_customer_country', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)    
    def __str__(self):
        return '%s' % (self.fullname)   

class rez(models.Model):
    product =  models.ForeignKey(product, related_name='rel_rez_product', on_delete=models.PROTECT)
    customer =  models.ForeignKey(customer, related_name='rel_rez_customer', on_delete=models.PROTECT)
    user =  models.ForeignKey(user, related_name='rel_rez_user', on_delete=models.PROTECT, null=True)
    confirmationNumber =  models.CharField(max_length=180, null=True)
    confirmationDate = models.DateTimeField(null=True)
    arrivalDate = models.DateTimeField(null=True)
    total = models.DecimalField(max_digits = 8,decimal_places = 2) 
    feeTotal = models.DecimalField(max_digits = 8,decimal_places = 2)
    feeAgency = models.DecimalField(max_digits = 8,decimal_places = 2) 
    feeUser = models.DecimalField(max_digits = 8,decimal_places = 2) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)    
    deleted_at = models.DateTimeField(null=True)


class payment(models.Model):
    rez =  models.ForeignKey(rez, related_name='rel_payment_rez', on_delete=models.PROTECT)
    prepaidDate = models.DateTimeField(null=True)
    payDate = models.DateTimeField(null=True)
    cancelationDate = models.DateTimeField(null=True)
    transactionNumber =  models.CharField(max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)    
    deleted_at = models.DateTimeField(null=True)


class audit(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    description =  models.CharField(max_length=255)
    user =  models.ForeignKey(user, related_name='rel_audit_user', on_delete=models.PROTECT)

class token(models.Model):
    date = models.DateField(null=True)
    user =  models.ForeignKey(user, related_name='rel_token_user', on_delete=models.PROTECT)
    token =  models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)    
    def __str__(self):
        return '%s' % (self.token)   
