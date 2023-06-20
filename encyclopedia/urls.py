from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"), #a request is sent to views.entry, default method is "GET", title is the input
    path("search/", views.search, name="search"), #request is sent to views.search
    path("new/", views.new_page, name="new_page"),
]
