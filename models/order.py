from django.db import models
from django.db.models import base
from django.db.models.deletion import CASCADE
from .user import CustomUser
from .card import Card
from .food import Food
from django.core.validators import validate_email

order_types = [('Pick-up', 'Pick-up'), ('Delivery', 'Delivery')]
payment_types = [('Card', 'Card'), ('Cash', 'Cash')]


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_timestamp = models.DateTimeField(auto_now_add=True)
    order_user = models.ForeignKey(CustomUser, on_delete=CASCADE)
    order_total = models.FloatField()
    order_tip = models.FloatField(null=True)
    order_delivery_fee = models.FloatField(null=True)
    order_type = models.CharField(max_length=10, choices=order_types)
    order_payment_type = models.CharField(max_length=10, choices=payment_types)
    order_card = models.ForeignKey(
        Card, on_delete=CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Order ID:{order}\nTotal: {total}'.format(order=self.order_id, total=self.order_total)


class GuestOrder(models.Model):
    guest_order_id = models.AutoField(primary_key=True)
    guest_order_timestamp = models.DateTimeField(auto_now_add=True)
    guest_order_name = models.CharField(max_length=100)
    guest_order_phone_number = models.CharField(max_length=20)
    guest_order_email = models.EmailField(validators=[validate_email])
    guest_order_total = models.FloatField()
    guest_order_tip = models.FloatField(null=True)
    guest_order_delivery_fee = models.FloatField(null=True)
    guest_order_type = models.CharField(max_length=10, choices=order_types)
    guest_order_payment_type = models.CharField(
        max_length=10, choices=payment_types)
    guest_order_card_number = models.CharField(
        max_length=20, null=True, blank=True)
    guest_order_card_exp_date = models.CharField(
        max_length=5, null=True, blank=True)
    guest_order_card_cvv = models.CharField(
        max_length=5, null=True, blank=True)
    guest_order_card_zipcode = models.CharField(
        max_length=5, null=True, blank=True)
    guest_order_street_number = models.CharField(
        max_length=10, null=True, blank=True)
    guest_order_street = models.CharField(max_length=50, null=True, blank=True)
    guest_order_apt = models.CharField(max_length=10, null=True, blank=True)
    guest_order_city = models.CharField(max_length=50, null=True, blank=True)
    guest_order_zipcode = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return 'Guest Order ID:{order}\nTotal: {total}'.format(order=self.guest_order_id, total=self.guest_order_total)


class OrderDetail(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    order_detail_order_id = models.ForeignKey(
        Order, on_delete=CASCADE, null=True)
    order_detail_guest_order_id = models.ForeignKey(
        GuestOrder, on_delete=CASCADE, null=True)
    order_detail_food = models.ForeignKey(Food, on_delete=CASCADE)
    order_detail_quantity = models.IntegerField()
    order_detail_options = models.TextField(
        max_length=100, null=True, blank=True)
    order_detail_price = models.FloatField()

    def __str__(self):
        return 'Order ID: {order}\nFood ID: {food}'.format(order=self.order_detail_order_id, food=self.order_detail_food)
