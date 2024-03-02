from rest_framework import serializers
from .models import Order, OrderDetails, Payment
from products.models import Product
from products.serializers import ProductSerializer


class OrderDetailsSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    order = serializers.StringRelatedField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderDetails
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()
    total = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'
        

    def get_details(self, obj):
        details = obj.orderdetails_set.all()
        order_details = []
        for detail in details:
            product_serializer = ProductSerializer(detail.product)
            order_detail = {
                'id':detail.pk,
                'product': product_serializer.data,
                'quantity': detail.quantity
            }
            order_details.append(order_detail)
        return order_details

    def get_total(self, obj):
        order_details = OrderDetails.objects.filter(order=obj)
        total = sum(
            [detail.price for detail in order_details])
        return total

    def get_items_count(self, obj):
        order_details = OrderDetails.objects.filter(order=obj)
        items_count = order_details.count()
        return items_count


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
