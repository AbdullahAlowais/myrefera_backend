# Generated by Django 4.1.7 on 2023-10-12 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CampaignApp', '0016_campaign_bank_account_campaign_fee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='bank_account',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='fee',
        ),
    ]
