from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from . serializers import RegistrationSerializer, CitySerializer, UserProfileSerializer, UserSerializer, ChangePasswordSerializer
from products.serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from . models import UserProfile, City
from products.models import Product
from rest_framework.exceptions import ValidationError
from orders.permissions import IsOrderUserOrReadOnly
from django.contrib import auth
from django.contrib.auth.hashers import make_password


@api_view(['POST',])
def logout(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response("Logged Out", status=status.HTTP_200_OK)


@permission_classes([AllowAny])
@api_view(['POST'])
def registration(request):
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data['response'] = "Registration Successful"
        data['username'] = user.username
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['email'] = user.email

        data['phone'] = user.userprofile.phone
        data['address'] = user.userprofile.address
        data['city'] = user.userprofile.city.name

        data['is_active'] = user.is_active

        token = Token.objects.get(user=user).key
        data['token'] = token

        return Response(data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == 'GET':
        userprofile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(userprofile)
        return Response(serializer.data)
    if request.method == 'PUT':
        user = request.user
        userprofile = UserProfile.objects.get(user=user)

        user_serializer = UserSerializer(user, data=request.data, partial=True)
        userprofile_serializer = UserProfileSerializer(
            userprofile, data=request.data, partial=True)

        user_serializer.is_valid()
        userprofile_serializer.is_valid()

        if user_serializer.is_valid() and userprofile_serializer.is_valid():
            user_serializer.save()
            userprofile_serializer.save()

            response_data = {
                # 'user': user_serializer.validated_data,
                'user_profile': userprofile_serializer.validated_data
            }
            return Response(response_data)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
@permission_classes([IsAuthenticated])
def product_favorite(request, product_id):
    product_favorite = Product.objects.get(pk=product_id)
    serializer = ProductSerializer(product_favorite)
    if UserProfile.objects.filter(user=request.user, product_favorites=product_favorite).exists():
        raise ValidationError("Product already in your favorites")

    else:
        userprofile = UserProfile.objects.get(user=request.user)
        userprofile.product_favorites.add(product_favorite)
        serializer = UserProfileSerializer(userprofile)
        return Response("Product added to your favorites", status=status.HTTP_200_OK)


@api_view(['GET',])
@permission_classes([IsOrderUserOrReadOnly])
def show_products_favorite(request):
    userInfo = UserProfile.objects.get(user=request.user)
    product_favorite = userInfo.product_favorites.all()
    serializer = ProductSerializer(product_favorite, many=True)
    response_data = {
        'product_favorite': serializer.data
    }
    return Response(response_data)


@api_view(['DELETE',])
@permission_classes([IsOrderUserOrReadOnly])
def remove_from_favorites(request, product_id):
    if product_id:
        product_favorite = Product.objects.get(pk=product_id)
        userInfo = UserProfile.objects.get(
            user=request.user, product_favorites=product_favorite)
        userInfo.product_favorites.remove(product_favorite)
    return Response("Product removed from your favorites",status=status.HTTP_200_OK)


@api_view(['PUT',])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    if request.method == 'PUT':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(user, serializer.validated_data)
            return Response({'message': 'Password updated successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET',])
@permission_classes([AllowAny])
def cities(request):
    categories = City.objects.all()
    serializer = CitySerializer(categories, many=True)
    response_data = {
        'cities': serializer.data
    }

    return Response(response_data)