from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Sum

from .form import Form, bid_form

from .models import User, Listing, Bid, Comment, Watchlist


def index(request):
    auctions = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auctions
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "POST":
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            category = form.cleaned_data["category"]
            description = form.cleaned_data["description"]
            bid = form.cleaned_data["bid"]
            img = form.cleaned_data["image"]
            user_listing = Listing(name=title, description=description,price=bid, category=category, image=img)
            user_listing.save()
        else:
            return render(request, "templates/auctions/create.html",{
                "Form" : form
            } )


    form = Form()
    return render(request, "auctions/create.html", {
       "Form" : form 
    })

def auction_listing(request, listing_id):  
    price = 0
    auction = Listing.objects.get(pk=listing_id)
    bids = auction.bids.count()
    db_bids = auction.bids.values()
    db_bid = 0
    for bid in db_bids:
        if db_bid < bid["price"]:
            db_bid = bid["price"]
    form = bid_form()
    db_bid = db_bid + 1
    if db_bid == 1:
        price = Listing.objects.values("price").filter(id=listing_id)
        db_bid = float(price[0]["price"])


    if request.method == "POST":
        form = bid_form(request.POST)
        user_bid = float(request.POST.get("user_bid"))

        if (form.is_valid() and db_bid < user_bid and price == 0) or (form.is_valid() and db_bid <= user_bid and price != 0):
            b = form.cleaned_data["user_bid"]
            db_save = Bid(price=b, listing_id=listing_id)
            db_save.save()
            bids = auction.bids.count()
            form.fields['user_bid'].widget.attrs.update({'min': db_bid})
            return render(request, "auctions/listing.html",{
                        "form" : form,
                        "auction" : auction,
                        "bids" : bids,
                        "context1" : "Bid Added Successfully!"
                        })
        else:
            form.fields['user_bid'].widget.attrs.update({'min': db_bid})
            return render(request, "auctions/listing.html",{
                        "form" : form,
                        "auction" : auction,
                        "bids" : bids,
                        "context2" : "Enter a Valid Bid!"

                        })
    form.fields['user_bid'].widget.attrs.update({'min': db_bid})
   
    return render(request, "auctions/listing.html", {
        "auction" : auction,
        "form" : form,
        "bids" : bids,
    })
def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST.get("watchlist")
        l = Listing.objects.get(pk=listing_id)
        
        watchlist = Watchlist(listing=l)
        watchlist.save()
        url = reverse("watchlist")
        return HttpResponseRedirect(url)
    listings = Listing.objects.all()
    auctions = []
    for listing in listings:
        watchlist = listing.watchlist.all()
        watchlist = watchlist.values()
        if watchlist:
            for _ in watchlist:
                watchlist = _["listing_id"]  
            listing = Listing.objects.get(pk=watchlist)
            auctions.append(listing)

    return render(request, "auctions/watchlist.html",{
        "auctions" : auctions
    })