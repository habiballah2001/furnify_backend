from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('registration/', views.registration, name='register'),
    path('profile/', views.profile, name='profile'),
    path('cities/', views.cities, name='cities'),

    path('change_password/', views.change_password, name='change_password'),
    path('product_favorite/<int:product_id>/',views.product_favorite, name='product_favorite'),

    path('show_products_favorite/', views.show_products_favorite,name='show_products_favorite'),
    path('remove_from_favorites/<int:product_id>/',views.remove_from_favorites, name='remove_from_favorites'),

    path('logout/', views.logout, name='logout'),

]
