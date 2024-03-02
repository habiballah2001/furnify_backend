from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from rest_framework.response import Response
from .models import Product, Category, Review
from rest_framework.permissions import IsAuthenticated,  AllowAny
from django.db.models import Q
from rest_framework import status


@api_view(['GET',])
@permission_classes([AllowAny])
def categories_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    response_data = {
        'categories': serializer.data
    }

    return Response(response_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    response_data = {
        'products': serializer.data
    }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([AllowAny])
def product_on_sale(request):
    products = Product.objects.all().filter(on_sale=True)
    serializer = ProductSerializer(products, many=True)
    response_data = {
        'products': serializer.data
    }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([AllowAny])
def search_products(request):
    search_query = request.GET.get('search')
    queryset = Product.objects.all()
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(price__icontains=search_query)
        )
    serializer = ProductSerializer(queryset, many=True)
    response_data = {
        'product': serializer.data
    }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([AllowAny])
def search_categories(request):
    search_query = request.GET.get('search')
    queryset = Category.objects.all()
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query)
        )
    serializer = CategorySerializer(queryset, many=True)
    response_data = {
        'category': serializer.data
    }
    return Response(response_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_products_in_category(request,category_id):
    search_query = request.GET.get('search')
    queryset = Product.objects.all().filter(category=category_id)
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(price__icontains=search_query)
        )
    serializer = ProductSerializer(queryset, many=True)
    response_data = {
        'product': serializer.data
    }
    return Response(response_data)


@api_view(['GET'])
def top_rated(request):
    products = Product.objects.all().filter(avg_rating__gte=4.5, avg_rating__lte=5.0).order_by('-avg_rating')
    serializer = ProductSerializer(products, many=True)
    response_data = {
        'products': serializer.data
    }
    return Response(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

    review_user = request.user
    review_queryset = Review.objects.filter(product=product, review_user=review_user)
    if review_queryset.exists():
        return Response({"error": "You have already reviewed this product"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        if product.number_rating == 0:
            product.avg_rating = serializer.validated_data['rating']
        else:
            product.avg_rating = (product.avg_rating +serializer.validated_data['rating'])/2
        product.number_rating = product.number_rating + 1
        product.save()

        serializer.save(product=product, review_user=review_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



