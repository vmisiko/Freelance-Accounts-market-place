# Generated by Django 2.2.5 on 2020-06-26 00:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=100)),
                ('apartment_address', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('zip_code', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=20, null=True, region=None)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('title', models.CharField(max_length=100)),
                ('price', models.FloatField(default=0.0)),
                ('discountprice', models.FloatField(blank=True, null=True)),
                ('category', models.CharField(choices=[('sw', 'Take Account'), ('OW', 'Transcribing Account'), ('s', 'Bidding Account')], max_length=2)),
                ('label', models.CharField(choices=[('D', 'danger'), ('S', 'secondary'), ('P', 'primary')], max_length=1)),
                ('Level', models.CharField(blank=True, choices=[('Juniour', 'Junior'), ('r', 'Seni0r'), ('Intermediate', 'Intermediate'), ('Ivy', 'Ivy')], max_length=15, null=True)),
                ('finished_orders', models.IntegerField(default=1)),
                ('rating', models.IntegerField(default=50)),
                ('Reviews', models.IntegerField(default=1)),
                ('profile', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('diplay_pic', models.ImageField(max_length=255, upload_to='display_pics/%Y%m%d/')),
                ('contact', models.CharField(blank=True, max_length=15, null=True)),
                ('sold', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('price', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('ordered', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField()),
                ('ordered', models.BooleanField(default=False)),
                ('amount', models.IntegerField(default=0.0)),
                ('released', models.BooleanField(default=False)),
                ('refund', models.BooleanField(default=False)),
                ('billing_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Home.BillingAddress')),
                ('items', models.ManyToManyField(to='Home.OrderItem')),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
