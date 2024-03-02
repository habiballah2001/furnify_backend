from rest_framework import serializers
from .models import Banner


class BannerSerializer(serializers.ModelSerializer):
    banner = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Banner
        fields = ['id', 'name', 'banner']
