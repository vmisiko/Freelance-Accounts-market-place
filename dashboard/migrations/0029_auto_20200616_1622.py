# Generated by Django 2.2.5 on 2020-06-16 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0028_auto_20200616_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawpayouts',
            name='payment_mode',
            field=models.CharField(choices=[('p', 'Paypal'), ('M', 'Mpesa')], max_length=20),
        ),
    ]