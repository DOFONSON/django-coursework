from django.contrib import admin
from django.urls import path
from goods import views
app_name = 'catalog'
urlpatterns = [
    path('<slug:company_slug>/', views.catalog, name='index'),
    path('<slug:company_slug>/<int:page>/', views.catalog, name='index'),
    path('product/<slug:product_slug>/', views.product, name='product')
]
