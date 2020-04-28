# Generated by Django 2.2.5 on 2020-03-26 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='Level',
            field=models.CharField(blank=True, choices=[('r', 'Seni0r'), ('Intermediate', 'Intermediate'), ('Ivy', 'Ivy'), ('Juniour', 'Junior')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('sw', 'Take Account'), ('OW', 'Transcribing Account'), ('s', 'Bidding Account')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('D', 'danger'), ('P', 'primary'), ('S', 'secondary')], max_length=1),
        ),
    ]