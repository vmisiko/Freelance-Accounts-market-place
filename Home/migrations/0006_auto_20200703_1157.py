# Generated by Django 2.2.5 on 2020-07-03 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0005_auto_20200630_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='Level',
            field=models.CharField(blank=True, choices=[('Senior', 'Senior'), ('Juniour', 'Junior'), ('Ivy', 'Ivy'), ('Intermediate', 'Intermediate')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('s', 'Bidding Account'), ('OW', 'Transcribing Account'), ('sw', 'Take Account')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('D', 'danger'), ('P', 'primary'), ('S', 'secondary')], max_length=1),
        ),
    ]
