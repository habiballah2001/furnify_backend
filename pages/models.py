from django.db import models

# Create your models here.


class Banner(models.Model):
    name = models.CharField(max_length=100)
    banner = models.ImageField(upload_to='photos/banners/%Y/%m/%d/')

    def __str__(self):
        return self.name
