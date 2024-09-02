from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1000)
    price = models.FloatField()
    image = models.ImageField(blank=True, null=True, upload_to='images/')
    time = models.DateTimeField(auto_now_add=True)
    category = models.CharField(blank=True, null=True,max_length=100)


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", default=0)
    price = models.FloatField()

    def __str__(self):
        return f"{self.listing} has a bid of {self.price}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", null=True)
    text = models.CharField(max_length=500)


class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist")