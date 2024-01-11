from rest_framework import status
from django.shortcuts import render
from .models import Category, Product, MyUser, Cart, CartItem, Order
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, CartItemSerializer
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import json

@api_view(['POST'])
def register(request):
    try:
        
        body_unicode = request.body.decode('utf-8')
        body=json.loads(body_unicode)
        username=body.get('username', None)
        email=body.get('email', None)
        first_name=body.get('first_name', None)
        last_name=body.get('last_name', None)
        password=body.get('password', None)
        if username is None or email is None or first_name is None or last_name is None or password is None:
            return Response('missing required fields - username, email, first_name, last_name, password', status=status.HTTP_400_BAD_REQUEST)
        existing_username=MyUser.objects.filter(username=username)

        if len(existing_username) > 0:
            return Response(f'username {username} already exist', status=status.HTTP_400_BAD_REQUEST)
        
        existing_email=MyUser.objects.filter(email=email)

        if len(existing_email) > 0:
            return Response(f'email {email} already exist', status=status.HTTP_400_BAD_REQUEST)
        
        user=MyUser(username=username,email=email,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save()
        return Response('user created', status=status.HTTP_201_CREATED)
    except Exception as ex:
        return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def cart_items(request):
    if request.method == 'GET':
        cart_items=[]
        try:
            cart=Cart.objects.get(user=request.user,is_paid=False)
            cart_items=CartItem.objects.filter(cart=cart)
            cart_items_json = CartItemSerializer(cart_items, many=True).data
            return Response(cart_items_json, status=status.HTTP_200_OK)  
        except Cart.DoesNotExist:
            return Response(cart_items, status=status.HTTP_200_OK)    
        except Exception as ex:
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    if request.method == 'POST':
        try:
           body_unicode = request.body.decode('utf-8')
           body=json.loads(body_unicode)
           product_id=body.get('product_id', None)
           quantity=body.get('quantity', None) 

           if product_id is None or quantity is None:
               return Response('missing required fields - product_id, quantity', status=status.HTTP_400_BAD_REQUEST)
           
           try:
               product_id=int(product_id)
               quantity=int(quantity)
               if product_id <= 0 or quantity <= 0:
                   raise 'ex'
           except:
               return Response('input validation fields failed - product_id, quantity', status=status.HTTP_400_BAD_REQUEST)
           product=Product.objects.get(id=product_id)
           try:
               cart=Cart.objects.get(user=request.user, is_paid=False)
           except Cart.DoesNotExist:
               cart=Cart(user=request.user)
               cart.save()
           try:
               cart_item=CartItem.objects.get(cart=cart, product=product)
               cart_item.quantity+=quantity
           except CartItem.DoesNotExist:
               cart_item=CartItem(product=product, quantity=quantity, cart=cart)
           cart_item.save() 
           return Response(status=status.HTTP_201_CREATED)     
            
        except Product.DoesNotExist:
            return Response('product_id does not exist', status=status.HTTP_404_NOT_FOUND) 
        except Exception as ex:
            return Response(ex, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
        
    
@api_view(['GET', 'POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
def products(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        maxprice = request.GET.get('maxprice')
        category = request.GET.get('category')
        all_products = Product.objects.all()
        # search all product that name contains search parameter
        if search:
            all_products = all_products.filter(name__contains=search)
        # search all product that price <= maxprice (price__lte=maxprice)
        if maxprice:
            all_products = all_products.filter(price__lte=maxprice)
        if category:
            all_products = all_products.filter(category__id=category)

        all_products_json = ProductSerializer(all_products, many=True).data
        return Response(all_products_json)
    elif request.method == 'POST':
        # this line creates a serializer object from json data
        serializer = ProductSerializer(data=request.data)
        # this line checkes validity of json data
        if serializer.is_valid():
            # the serializer.save - saves a new product object
            serializer.save()
            # returns the object that was created including id
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if not valid. return errors.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    # get object from db by id
    try:
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # GET
    if request.method == 'GET':
        # create serializer from object
        serializer = ProductSerializer(product)
        # return json using serializer
        return Response(serializer.data)
    # PUT
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DELETE
    elif request.method == 'DELETE':
        # product.is_active = False
        # product.save()
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def categories(request):
    search = request.GET.get('search')
    all_categories = Category.objects.all()
    if search:
        all_categories = all_categories.filter(name__contains=search)
    all_categories_json = CategorySerializer(all_categories, many=True).data
    return Response(all_categories_json)
