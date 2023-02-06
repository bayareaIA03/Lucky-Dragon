from django.contrib import admin
from .models.user import CustomUser
from .models.food import Food
from .models.order import Order, GuestOrder, OrderDetail
from .models.card import Card

from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(GuestOrder)
admin.site.register(Card)
