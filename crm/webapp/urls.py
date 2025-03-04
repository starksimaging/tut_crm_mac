from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views. login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('client/<int:pk>/', views.client, name='client'),
    path('client_delete/<int:pk>/', views.client_delete, name='client_delete'),
    path('add_client/', views.add_client, name='add_client'),
    path('client_update/<int:pk>/', views.client_update, name='client_update'),
    path('client/products/<int:pk>/', views.products_purchased, name='products_purchased'),
    path('add_product/<int:client_id>/', views.add_product, name='add_product'),
    path('inventory/', views.inventory, name='inventory'),
]
