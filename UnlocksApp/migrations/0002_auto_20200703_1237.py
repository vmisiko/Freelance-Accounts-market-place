# Generated by Django 2.2.5 on 2020-07-03 09:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UnlocksApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='unlocks',
            name='full_Names',
            field=models.CharField(default='victor Misiko', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='unlocks',
            name='category',
            field=models.CharField(choices=[('Scrbd', 'Scrbd Unlock'), ('CourseHero', 'CourseHero Unlock'), ('Chegg', 'chagg Unlock')], max_length=20),
        ),
        migrations.CreateModel(
            name='Logins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_Names', models.CharField(max_length=500)),
                ('category', models.CharField(choices=[('CourseHero', 'CourseHero Logins'), ('Scrbd', 'Scrbd Logins'), ('Netflix Logins', 'Netflix Logins'), ('Nord', 'Nord VPN'), ('Chegg', 'chagg Logins'), ('Turnitin', 'Turnitin Logins'), ('DSTV', 'DSTV'), ('Grammarly', 'Grammarly Premium')], max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('other', models.CharField(max_length=500)),
                ('status', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
