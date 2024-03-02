from rest_framework import serializers
from .models import Service, Service_Category


class Service_CategorySerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(max_length=None, use_url=True)


    class Meta:
        model = Service_Category
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(max_length=None, use_url=True)
    name = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    class Meta:
            model = Service
            fields = '__all__'


