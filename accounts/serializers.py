from rest_framework import serializers
from django.contrib.auth.models import User
from .models import City, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    phone = serializers.CharField(write_only=True)
    address = serializers.CharField(write_only=True)
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), write_only=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password','password2', 'phone', 'address', 'city', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2', None)

        if password != password2:
            raise serializers.ValidationError(
                {'error': "Passwords doesn't match"})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {'error': 'Email already exists'})

        return data

    def create(self, validated_data):
        phone = validated_data.pop('phone', None)
        address = validated_data.pop('address', None)
        city = validated_data.pop('city', None)

        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        user_profile = UserProfile(
            user=user, phone=phone, city=city, address=address)
        user_profile.save()

        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    phone = serializers.CharField()
    city = serializers.CharField(source='city.name')

    class Meta:
        model = UserProfile
        # fields = '__all__'
        exclude = ['product_favorites']

    def update(self, instance, validated_data):
        city_data = validated_data.pop('city', None)
        if city_data:
            city_name = city_data.get('name')
            if city_name:
                city = City.objects.get(name=city_name)
                instance.city = city

        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2', None)

        if password != password2:
            raise serializers.ValidationError(
                {'error': "Passwords doesn't match"})
        return data

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if not password.startswith('pbkdf2_sha256$'):
            instance.set_password(password)
        instance.save()
        return instance
