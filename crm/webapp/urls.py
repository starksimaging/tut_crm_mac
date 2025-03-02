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

]
