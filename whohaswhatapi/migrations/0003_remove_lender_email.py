# Generated by Django 4.0.3 on 2022-03-11 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whohaswhatapi', '0002_alter_item_price_per_day_alter_item_price_per_week'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lender',
            name='email',
        ),
    ]
