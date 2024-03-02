from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_categories_list, name='service_categories_list'),
    path('services/', views.services, name='services'),


]
