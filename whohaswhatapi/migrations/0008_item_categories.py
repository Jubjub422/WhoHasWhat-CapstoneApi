# Generated by Django 4.0.3 on 2022-03-17 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whohaswhatapi', '0007_requestqueue'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='categories',
            field=models.ManyToManyField(related_name='categories', through='whohaswhatapi.ItemCategory', to='whohaswhatapi.category'),
        ),
    ]
