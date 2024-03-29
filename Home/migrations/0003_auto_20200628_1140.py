# Generated by Django 2.2.5 on 2020-06-28 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_auto_20200627_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='Level',
            field=models.CharField(blank=True, choices=[('Juniour', 'Junior'), ('Intermediate', 'Intermediate'), ('Ivy', 'Ivy'), ('r', 'Seni0r')], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('s', 'Bidding Account'), ('OW', 'Transcribing Account'), ('sw', 'Take Account')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('P', 'primary'), ('D', 'danger'), ('S', 'secondary')], max_length=1),
        ),
    ]
