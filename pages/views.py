from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .models import Banner
from .serializers import BannerSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@permission_classes([AllowAny])
@api_view(['GET',])
def banners(request):
    banner = Banner.objects.all()
    serializer = BannerSerializer(banner, many=True)
    response_data = {
        'banners': serializer.data
    }

    return Response(response_data)
