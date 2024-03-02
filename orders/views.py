from django.shortcuts import render, redirect, reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from products.serializers import ProductSerializer
from .models import Order, OrderDetails, Payment
from .serializers import OrderSerializer, OrderDetailsSerializer, PaymentSerializer
from rest_framework.response import Response
from django.contrib import messages
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .permissions import IsOrderUserOrReadOnly
from products.models import Product


@api_view(['POST',])
@permission_classes([IsOrderUserOrReadOnly])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')

    if not product_id or not quantity:
        return Response({'error': 'Missing product_id or quantity.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        order = Order.objects.filter(
            user=request.user, is_finished=False).exists()
        product = Product.objects.get(pk=product_id)

        if order == True:
            order = Order.objects.get(user=request.user, is_finished=False)
            orderdetails = OrderDetails.objects.filter(
                order=order, product=product).exists()
            if orderdetails == True:
                # Update the existing order details
                order_details = OrderDetails.objects.get(
                    order=order, product=product)
                order_details.quantity += int(quantity)
                order_details.price = int(quantity)*product.price
                order_details.save()
            else:
                order_details = OrderDetails.objects.create(
                    order=order, product=product, price=product.price, quantity=quantity)
        else:
            # Create a new order and order details objects
            order = Order.objects.create(
                user=request.user, order_date=timezone.now(), is_finished=False)
            order_details = OrderDetails.objects.create(
                order=order, product=product, price=int(quantity)*product.price, quantity=quantity)
            order_details_serializer = OrderDetailsSerializer(
                data=order_details)

            if order_details_serializer.is_valid():
                order_details_serializer.save()
                order_serializer = OrderSerializer(order)
                response_data = {
                    'order': order_serializer.data,
                    'order_details': order_details_serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

        # Return a redirect response to the cart page
        return Response("Added to your Cart", headers={'Location': reverse('cart')})


@api_view(['GET',])
@permission_classes([IsOrderUserOrReadOnly])
def cart(request):
    if Order.objects.filter(user=request.user, is_finished=False).exists():
        order = Order.objects.get(user=request.user, is_finished=False)
        serializer = OrderSerializer(order, partial=True)
        # Exclude the "details" field
        serializer.fields['details'].read_only = True
        order_details = OrderDetails.objects.filter(order=order).select_related('product')
        order_details_serializer = OrderDetailsSerializer(order_details, many=True)
        total = sum(sub.price * sub.quantity for sub in order_details)
        response_data = {
            'cart': serializer.data
        }

        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        order = Order.objects.create(user=request.user, order_date=timezone.now(), is_finished=False)
        serializer = OrderSerializer(order, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['DELETE',])
@permission_classes([IsOrderUserOrReadOnly])
def remove_from_cart(request, orderdetails_id):
    if orderdetails_id:
        orderdetails = OrderDetails.objects.get(id=orderdetails_id)
        if orderdetails.order.user.id == request.user.id:
            orderdetails.delete()
    return Response("Item removed from your cart", status=status.HTTP_200_OK, headers={'Location': reverse('cart')})


@api_view(['DELETE',])
@permission_classes([IsOrderUserOrReadOnly])
def delete_cart(request):
    cart_exists = Order.objects.filter(
        user=request.user, is_finished=False).exists()
    if cart_exists:
        order = Order.objects.get(user=request.user, is_finished=False)
        order.delete()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response("No items in your cart", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
@permission_classes([IsOrderUserOrReadOnly])
def add_quantity(request, orderdetails_id):
    orderdetails = OrderDetails.objects.get(id=orderdetails_id)
    if orderdetails.order.user.id == request.user.id:
        orderdetails.quantity = orderdetails.quantity + 1
        orderdetails.save()
        orderdetails_serializer = OrderDetailsSerializer(orderdetails)
        response_data = {
            'orderdetails': orderdetails_serializer.data
        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED, headers={'Location': reverse('cart')})
    else:
        return Response({'error': 'You do not have permission to add quantity to this orderdetail.'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST',])
@permission_classes([IsOrderUserOrReadOnly])
def sub_quantity(request, orderdetails_id):
    orderdetails = OrderDetails.objects.get(id=orderdetails_id)
    if orderdetails.order.user.id == request.user.id:
        orderdetails.quantity -= 1
        orderdetails.save()
        orderdetails_serializer = OrderDetailsSerializer(orderdetails)
        response_data = {
            'orderdetails': orderdetails_serializer.data
        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED, headers={'Location': reverse('cart')})
    else:
        return Response({'error': 'You do not have permission to add quantity to this orderdetail.'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET',])
@permission_classes([IsOrderUserOrReadOnly])
def show_orders(request):
    all_orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(all_orders, many=True)
    response_data = {
        'orders': serializer.data
    }
    return Response(response_data)


@api_view(['POST',])
@permission_classes([IsOrderUserOrReadOnly])
def payment(request):
    if not Order.objects.filter(user=request.user, is_finished=False).exists():
        return Response("You don't have any active order to make a payment.")

    # if all required fields are provided in the request data
    if all(key in request.data for key in ('shipment_address', 'shipment_phone', 'card_number', 'expire', 'security_code')):
        order = Order.objects.get(user=request.user, is_finished=False)
        serializer = OrderSerializer(order)

        # create payment object and save it to the database
        payment_serializer = PaymentSerializer(
            data=request.data, partial=True)
        if payment_serializer.is_valid():
            payment_serializer.save(order=order)
            order.is_finished = True
            order.save()
            return Response("Your order is finished.")
        else:
            return Response(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        order = Order.objects.get(user=request.user, is_finished=False)
        order_serializer = OrderSerializer(order)
        order_details = OrderDetails.objects.filter(order=order)
        order_details_serializer = OrderDetailsSerializer(
            order_details, many=True)
        total = sum(sub.price * sub.quantity for sub in order_details)

        context = {
            'order': order_serializer.data,
            'order_details': order_details_serializer.data,
            'total': total,
        }
        return Response(context)
