from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers


router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('accounts/', include('accounts.urls')),
    path('services/', include('services.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
