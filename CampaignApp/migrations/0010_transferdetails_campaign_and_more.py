# Generated by Django 4.2.1 on 2023-07-20 06:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CampaignApp', '0009_campaign_payout_amount_product_information_coupon_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferdetails',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CampaignApp.campaign'),
        ),
        migrations.AddField(
            model_name='transferdetails',
            name='remaining_amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]