# Generated by Django 3.0.6 on 2021-07-24 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luckydragon_app', '0005_auto_20210724_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_phone_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]