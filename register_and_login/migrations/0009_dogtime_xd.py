# Generated by Django 3.1.4 on 2020-12-30 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register_and_login', '0008_auto_20201230_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='dogtime',
            name='xd',
            field=models.BooleanField(default=False),
        ),
    ]