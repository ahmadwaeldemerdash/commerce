# Generated by Django 5.1 on 2024-09-06 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0033_listing_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
