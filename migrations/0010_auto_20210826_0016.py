# Generated by Django 3.1.4 on 2021-08-26 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luckydragon_app', '0009_auto_20210825_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='food_category',
            field=models.CharField(choices=[('Appetizer', 'Appetizer'), ('Soup', 'Soup'), ('Fried Rice', 'Fried Rice'), ('Lo Mein', 'Lo Mein'), ('Chow Mein', 'Chow Mein'), ('Egg Foo Young', 'Egg Foo Young'), ('Specialty Noodle', 'Specialty Noodle'), ('Japanese Kitchen', 'Japanese Kitchen'), ('Traditional Plate', 'Traditional Plate'), ('Vegetable', 'Vegetable'), ('House Specialty', 'House Specialty'), ('Thai Kitchen', 'Thai Kitchen'), ('Dinner Special', 'Dinner Special'), ('Lunch Special', 'Lunch Special'), ('Lunch Fried Rice', 'Lunch Fried Rice'), ('Lunch Noodle', 'Lunch Noodle'), ('Drink', 'Drink'), ('Dessert', 'Dessert'), ('Free', 'Free')], max_length=30),
        ),
    ]
