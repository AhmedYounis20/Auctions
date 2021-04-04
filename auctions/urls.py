from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path("", RedirectView.as_view(url='listings'), name="index"),
    path("listings", views.index, name="index"),
    path("listings/<int:num>", views.listview, name="product"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categoriesview, name="categories"),
    path("categories/<slug:cat>", views.categoryview, name="category"),

    path("createlisting", views.createlistingview, name="createlisting"),

    path("watchlist", views.watchlistview, name="watchlist"),


]
