from django.urls import include, path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path(
        "tag/<str:tag_name>/page/<int:page>/", views.quotes_by_tag, name="quotes_by_tag"
    ),
    path("author/<slug:author_slug>/", views.author_page, name="author_page"),
    path("users/", include("users.urls")),
]
