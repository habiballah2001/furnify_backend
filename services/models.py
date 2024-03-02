from django.db import models


class Service_Category (models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='photos/service_category/%Y/%m/%d/')
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return self.name


class Service (models.Model):
    name = models.ForeignKey(
        Service_Category, on_delete=models.CASCADE, related_name='service')
    description = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/service/%Y/%m/%d/', null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

