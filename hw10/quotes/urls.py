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
    path("add_author/", views.add_author, name="add_author"),
    path("add_quote/", views.add_quote, name="add_quote"),
    path("scrape_quotes/", views.scrape_quotes, name="scrape_quotes"),
    path("search_results/", views.search_results, name="search_results"),
    path("fill_base/", views.fill_base, name="fill_base"),
]
