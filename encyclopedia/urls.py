from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random, name="random"),
    path("newentry", views.newentry, name="newentry"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("<str:title>", views.wikientry, name="wikientry")

]
