# Generated by Django 4.2.1 on 2023-10-23 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CampaignApp', '0024_feepaid_influ_amount_alter_feepaid_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feepaid',
            name='influ_amount',
            field=models.CharField(default=0, max_length=255),
        ),
    ]
