# Generated by Django 4.0.3 on 2022-03-17 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whohaswhatapi', '0004_lender_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='pending_approval',
            field=models.BooleanField(default=False),
        ),
    ]