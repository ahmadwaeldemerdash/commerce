# Generated by Django 5.1 on 2024-08-31 12:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_bid_listing_comments_listing_alter_bid_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.auction_listing'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='listing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.auction_listing'),
        ),
    ]
