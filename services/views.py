from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Service, Service_Category
from .serializers import ServiceSerializer, Service_CategorySerializer


@api_view(['GET',])
@permission_classes([AllowAny])
def service_categories_list(request):
    service_categories = Service_Category.objects.all()
    serializer = Service_CategorySerializer(service_categories, many=True)
    response_data = {
        'service_category': serializer.data
    }
    return Response(response_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def services(request):
    serializer = ServiceSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response_data = {
            'data': serializer.data
        }
        return Response(response_data)
    else:
        return Response(serializer.errors)


