# Generated by Django 4.1.7 on 2023-10-16 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0004_user_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='facility',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
