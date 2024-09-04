from django.contrib import admin
from .models import Listing, Bid, Comment, Watchlist, User, Category, Winner
# Register your models here.
class listingAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
admin.site.register(User)
admin.site.register(Listing, listingAdmin)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Watchlist)
admin.site.register(Category)
admin.site.register(Winner)