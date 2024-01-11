from rest_framework import serializers
from .models import Category, Product, MyUser, Order, Cart, CartItem

class CategorySerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    class Meta:
        model = Product
        fields = '__all__' 
        # example of how to filter fields. remove line 7 __all__ and replace with line 9:
        # fields = ['name','price']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'first_name', 'last_name'] 
        # example of how to filter fields. remove line 7 __all__ and replace with line 9:
        # fields = ['name','price']        

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Cart
        fields = '__all__' 
        # example of how to filter fields. remove line 7 __all__ and replace with line 9:
        # fields = ['name','price']      

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    cart = CartSerializer(many=False, read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__' 
        # example of how to filter fields. remove line 7 __all__ and replace with line 9:
        # fields = ['name','price']            


