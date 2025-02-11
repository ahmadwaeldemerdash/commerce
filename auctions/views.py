from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max


from .form import Form, bid_form

from .models import User, Listing, Bid, Comment, Watchlist, Category, Winner


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
        user = request.POST.get("user")
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            try:
                category = Category.objects.get(pk=category)
            except:
                category = None
            price = form.cleaned_data["price"]
            img = form.cleaned_data["image"]
            user_listing = Listing(user=User.objects.get(username=user), name=title, description=description,price=price, category=category, image=img)
            user_listing.save()
            url = reverse("index")
            return HttpResponseRedirect(url)
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
    try:

        winner = Winner.objects.get(listing=auction)
    except:
        winner = None
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
    form.fields['user_bid'].widget.attrs.update({'min': db_bid})
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.all().filter(listing=listing)
    category = listing.category
    user = User.objects.get(username=request.user.username)
    if len(listing.watchlist.all().filter(user=user)) == 0:
        token = 0
    elif len(listing.watchlist.all().filter(user=user)) != 0:
        token = 1
    if request.method == "POST":
        form = bid_form(request.POST)
        user_bid = float(request.POST.get("user_bid"))
        user = User.objects.get(username=request.POST.get("user"))
        if (form.is_valid() and db_bid < user_bid and price == 0) or (form.is_valid() and db_bid <= user_bid and price != 0):
            b = form.cleaned_data["user_bid"]
            db_save = Bid(user=user, price=b, listing_id=listing_id)
            db_save.save()
            bids = auction.bids.count()
            form.fields['user_bid'].widget.attrs.update({'min': db_bid})
            return render(request, "auctions/listing.html",{
                "form" : form,
                "auction" : auction,
                "bids" : bids,
                "context1" : "Bid Added Successfully!", 
                "token" : token,
                "comments" : comments,
                "category" : category,
                "winner" : winner
            })
        else:
            form.fields['user_bid'].widget.attrs.update({'min': db_bid})
            return render(request, "auctions/listing.html",{
            "form" : form,
            "auction" : auction,
            "bids" : bids,
            "context2" : "Enter a Valid Bid!",
            "token" : token,
            "comments" : comments,
            "category" : category,
            "winner" : winner
            })
  
    
    return render(request, "auctions/listing.html", {
        "auction" : auction,
        "form" : form,
        "bids" : bids,
        "token" : token,
        "comments" : comments,
        "category" : category, 
        "winner" : winner
    })
def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST.get("watchlist")
        user = request.POST.get("user")
        user = User.objects.get(username=user)
        l = Listing.objects.get(pk=listing_id)
        watchlist = Watchlist(listing=l, user=user)
        watchlist.save()
        db_watchlists = Watchlist.objects.get(user=user)
        watchlist = []
        try:
            for w in db_watchlists:
                watchlist.append(w.listing)
        except:
            watchlist.append(db_watchlists.listing)
        return render(request, "auctions/index.html", {
            "auctions" : watchlist,
            "title" : "Watchlist"
        })
    listings = Listing.objects.all()
    auctions = []
    user = User.objects.get(username=request.user.username)
    for listing in listings:
        watchlist = listing.watchlist.all().filter(user=user)
        watchlist = watchlist.values()
        if watchlist:
            for _ in watchlist:
                watchlist = _["listing_id"]  
            listing = Listing.objects.get(pk=watchlist)
            auctions.append(listing)

    return render(request, "auctions/index.html",{
        "auctions" : auctions,
        "title" : "Watchlist",
    })


def remove(request):
    if request.method == "POST":
        listing = request.POST.get("remove")
        listing = Listing.objects.get(pk=listing)
        listing = listing.watchlist.all()
        listing.delete()
        url = reverse("watchlist")
        return HttpResponseRedirect(url)
    
def add_comment(request, listing_id):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.POST.get("name")
        user = User.objects.get(username=user)
        listing = Listing.objects.get(pk=listing_id)
        add = Comment(user=user, listing=listing, text=comment)
        add.save()
        url = reverse("listing" ,args=[listing_id])
        return HttpResponseRedirect(url)

def categories(request):
    categories = Category.objects.all()

    return render(request, "auctions/category.html", {
        "categories" : categories
    })

def listing_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.all().filter(category=category, active=True)
    return render(request, "auctions/index.html", {
        "auctions" : listings
    })

def close(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        listing.active = False
        listing.save()
        bids = listing.bids.all()
        sum = 0
        for bid in bids:
            if bid.price > sum :
                sum = bid.price
        try:
            b = Bid.objects.get(price=sum)
        except:
           listing.delete()
           url = reverse("index")
           return HttpResponseRedirect(url)
           #url = reverse("listing", args=[listing_id])
           #return HttpResponseRedirect(url)
        user = b.user
        winner = Winner(user=user, listing=listing)
        winner.save()
        try:
            watchlist = Watchlist.objects.get(listing=listing)
            watchlist.delete()
        except:
            watchlist = None
        url = reverse("listing", args=[listing_id])
        return HttpResponseRedirect(url)
