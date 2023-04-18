from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry_page, name="entry_page"),
    path("create/create_neinat", views.create_entry, name="create_entry"),
    path("edit/<str:title>", views.edit_entry, name="edit_entry"),
    path("random/random_page", views.random_page, name="random_page")
]
