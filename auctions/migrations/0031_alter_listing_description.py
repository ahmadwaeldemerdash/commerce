# Generated by Django 5.1 on 2024-09-05 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0030_alter_winner_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.CharField(max_length=5000),
        ),
    ]
