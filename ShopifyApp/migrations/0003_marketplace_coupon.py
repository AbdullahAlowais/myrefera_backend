# Generated by Django 4.2.1 on 2023-08-05 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ShopifyApp', '0002_alter_influencer_coupon_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marketplace_coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_name', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('coupon_id', models.CharField(blank=True, max_length=255, null=True)),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
