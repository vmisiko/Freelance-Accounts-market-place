# Generated by Django 2.2.5 on 2020-04-08 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_refund_reason'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refund',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]