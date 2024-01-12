from django.urls import path
from . import views
urlpatterns = [
    # product - for list of products and create product.
    path('product', views.products, name="products"), 
    path('product/<id>', views.product_detail, name="product_detail"), 
    path('category', views.categories, name="categories"),
    path('register', views.register),
    path('cart-items', views.cart_items),
    path('cart-item/<id>', views.cart_item),
    path('order', views.order)
]