# Generated by Django 4.2.5 on 2023-11-27 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0005_user_facility'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='commission',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
