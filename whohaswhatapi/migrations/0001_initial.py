# Generated by Django 4.0.3 on 2022-03-10 20:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=2)),
                ('price_per_week', models.DecimalField(decimal_places=2, max_digits=3)),
                ('rented_currently', models.BooleanField(default=False)),
                ('item_image', models.URLField(max_length=400)),
                ('condition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='whohaswhatapi.condition')),
            ],
        ),
        migrations.CreateModel(
            name='Lender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=125)),
                ('email', models.EmailField(max_length=250)),
                ('is_owner', models.BooleanField(default=False)),
                ('is_renter', models.BooleanField(default=True)),
                ('profile_image_url', models.URLField(max_length=500)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RentedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rented_on', models.DateField(auto_now_add=True)),
                ('return_by', models.DateField()),
                ('rental_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whohaswhatapi.item')),
                ('renter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='renter', to='whohaswhatapi.lender')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('rated', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rated', to='whohaswhatapi.lender')),
                ('rater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rater', to='whohaswhatapi.lender')),
            ],
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whohaswhatapi.category')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whohaswhatapi.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whohaswhatapi.lender'),
        ),
    ]
