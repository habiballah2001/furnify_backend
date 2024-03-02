from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='photos/product_category/')

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=20)
    percentage = models.PositiveIntegerField(validators=[MaxValueValidator(100)],null=True)

    def __str__(self):
        return self.name
    
class Provider(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photos/product/%Y/%m/%d/')
    model = models.FileField(upload_to='models/%Y/%m/%d/')
    description = models.CharField()
    price = models.FloatField()
    on_sale = models.BooleanField(default=False)
    old_price = models.FloatField(null=True,blank=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='product',default=0)
    provided_by = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name='product',default=1)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def calculate_price(self):
        if self.on_sale:
            if not self.old_price:
                self.old_price = self.price
            discount_percentage = self.discount.percentage
            discount_amount = (self.price * discount_percentage) / 100
            self.price -= discount_amount
        elif self.on_sale == False and self.old_price:
            self.price = self.old_price
            self.old_price = None
        self.save()


class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating) + " | " + self.product.name + " | " + str(self.review_user)
