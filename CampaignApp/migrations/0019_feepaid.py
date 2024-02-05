# Generated by Django 4.1.7 on 2023-10-17 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CampaignApp', '0018_influencerpaid'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeePaid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('adminfee', models.IntegerField(blank=True, null=True)),
                ('influecerid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vendorid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vendor1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]