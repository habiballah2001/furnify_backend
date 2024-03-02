from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    details = models.ManyToManyField(Product, through='OrderDetails')
    is_finished = models.BooleanField(default=False)
    total = models.FloatField(default=0)
    items_count = models.IntegerField(default=0)

    def calculate_total(self):
        total = 0
        for order_detail in self.orderdetails_set.all():
            total += order_detail.price * order_detail.quantity
        return total

    def __str__(self):
        return 'User: ' + self.user.username + ', Order id: ' + str(self.id)


class OrderDetails(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return 'User: '+self.order.user.username + ', Product:' + self.product.name + ', Order ID: ' + str(self.order.id)


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipment_address = models.CharField(max_length=150)
    shipment_phone = models.CharField(max_length=50)
    card_number = CardNumberField()
    expire = CardExpiryField()
    security_code = SecurityCodeField()

    def __str__(self):
        return self.name
