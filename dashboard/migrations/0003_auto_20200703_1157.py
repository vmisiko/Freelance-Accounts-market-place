# Generated by Django 2.2.5 on 2020-07-03 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20200628_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawpayouts',
            name='payment_mode',
            field=models.CharField(choices=[('M', 'Mpesa'), ('p', 'Paypal')], max_length=20),
        ),
    ]
