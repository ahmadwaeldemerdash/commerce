# Generated by Django 5.1 on 2024-09-06 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0032_watchlist_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='active',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
