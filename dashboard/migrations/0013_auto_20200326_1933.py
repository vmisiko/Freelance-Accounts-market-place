# Generated by Django 2.2.5 on 2020-03-26 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_auto_20200316_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawpayouts',
            name='payment_mode',
            field=models.CharField(choices=[('M', 'Mpesa'), ('p', 'Paypal')], max_length=20),
        ),
    ]