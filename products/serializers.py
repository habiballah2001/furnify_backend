from rest_framework import serializers
from .models import Category, Product, Review, Discount


class CategorySerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Category
        fields = '__all__'


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(max_length=None, use_url=True)
    model = serializers.FileField(max_length=None, use_url=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = '__all__'



class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ['product']
