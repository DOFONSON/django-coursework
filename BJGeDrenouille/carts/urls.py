from django.contrib import admin
from django.urls import path
from goods import views

app_name = 'carts'

urlpatterns = [
    path('cart_add/<int:product_id>', views.catalog, name='cart_add'),
    path('cart_change/<int:product_id>', views.catalog, name='cart_change'),
    path('cart_remove/<int:product_id>', views.product, name='cart_remove')
]
