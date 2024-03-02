from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    product_favorites = models.ManyToManyField(Product, null=True)
    address = models.CharField()
    phone = models.CharField(max_length=20)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="userprofile")

    def __str__(self):
        return self.user.username
