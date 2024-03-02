from django.urls import path
from . import views

urlpatterns = [
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove_from_cart/<int:orderdetails_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('delete_cart/', views.delete_cart, name='delete_cart'),
    path('add_quantity/<int:orderdetails_id>/',views.add_quantity, name='add_quantity'),
    path('sub_quantity/<int:orderdetails_id>/',views.sub_quantity, name='sub_quantity'),
    path('show_orders/', views.show_orders, name='show_orders'),
    path('payment/', views.payment, name='payment'),

]
