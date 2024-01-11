from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    pass

class Product(models.Model):
    
    category = models.ForeignKey('Category',on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100, null=False)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'
    
class Cart(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    is_paid=models.BooleanField(default=False)
    user=models.ForeignKey(MyUser, on_delete=models.CASCADE) 

    def __str__(self):
        return f'{self.creation_date} - {self.user} - {self.is_paid}'
    
class CartItem(models.Model):
    product=models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)   

class Order(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True) 
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE) 
    amount=models.DecimalField(max_digits=16, decimal_places=2) 

class Category(models.Model):    
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.name}'
    

