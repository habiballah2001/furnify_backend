from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='products_list'),
    path('categories/', views.categories_list, name='categories_list'),
    path('search_products_in_category/<int:category_id>/', views.search_products_in_category, name='search_products_in_category'),
    path('top_rated/', views.top_rated, name='top_rated'),
    path('product_on_sale/', views.product_on_sale, name='product_on_sale'),
    path('search_products/', views.search_products, name='search_products'),
    path('search_categories/', views.search_categories, name='search_categories'),
    path('<int:pk>/create_review/',views.create_review, name='review-create'),
]
