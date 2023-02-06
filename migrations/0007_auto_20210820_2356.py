# Generated by Django 3.1.4 on 2021-08-21 03:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('luckydragon_app', '0006_auto_20210724_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestorder',
            name='uest_order_timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 8, 21, 3, 55, 58, 723668, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='order_timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 8, 21, 3, 56, 15, 173492, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
