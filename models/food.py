from django.db import models
from django.contrib.auth.models import User


class Food(models.Model):
    categories = [('Appetizer', 'Appetizer'), ('Soup', 'Soup'), ('Fried Rice', 'Fried Rice'),
                  ('Lo Mein', 'Lo Mein'),
                  ('Chow Mein', 'Chow Mein'), ('Egg Foo Young', 'Egg Foo Young'),
                  ('Specialty Noodle', 'Specialty Noodle'),
                  ('Japanese Kitchen', 'Japanese Kitchen'),
                  ('Traditional Plate', 'Traditional Plate'),
                  ('Vegetable', 'Vegetable'), ('House Specialty', 'House Specialty'),
                  ('Thai Kitchen', 'Thai Kitchen'),
                  ('Dinner Special', 'Dinner Special'), ('Lunch Special', 'Lunch Special'),
                  ('Lunch Fried Rice', 'Lunch Fried Rice'),
                  ('Lunch Noodle', 'Lunch Noodle'),
                  ('Drink', 'Drink'), ('Dessert', 'Dessert'), ('Free', 'Free'),
                  ('Kids Menu', 'Kids Menu'), ('Sauces', 'Sauces')]
    food_id = models.AutoField(primary_key=True)
    food_price = models.FloatField(default=0)
    food_image = models.CharField(max_length=500, null=True, blank=True)
    food_name = models.CharField(max_length=100)
    food_description = models.TextField(max_length=1000, null=True, blank=True)
    food_category = models.CharField(max_length=30, choices=categories)
    food_spicy = models.BooleanField(default=False)
    food_op1 = models.CharField(max_length=100, null=True, blank=True)
    food_op2 = models.CharField(max_length=100, null=True, blank=True)
    food_op3 = models.CharField(max_length=100, null=True, blank=True)
    food_op4 = models.CharField(max_length=100, null=True, blank=True)
    food_op5 = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "Food Name: {name}\nPrice: {price}".format(name=self.food_name, price=self.food_price)
