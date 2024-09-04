from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("listing/<int:listing_id>/", views.auction_listing, name="listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("remove/", views.remove, name="remove"),
    path("comment/<int:listing_id>", views.add_comment, name="comment"),
    path("categories/", views.categories, name="categories"),
]
