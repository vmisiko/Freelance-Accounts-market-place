# Generated by Django 2.2.5 on 2020-05-23 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0023_auto_20200523_0315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawpayouts',
            name='payment_mode',
            field=models.CharField(choices=[('M', 'Mpesa'), ('p', 'Paypal')], max_length=20),
        ),
    ]