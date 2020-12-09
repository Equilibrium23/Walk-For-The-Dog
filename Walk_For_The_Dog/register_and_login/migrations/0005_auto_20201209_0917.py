# Generated by Django 3.1.3 on 2020-12-09 09:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('register_and_login', '0004_auto_20201208_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='joining_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='dog',
            name='short_description',
            field=models.CharField(max_length=300),
        ),
    ]
