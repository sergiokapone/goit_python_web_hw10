from django.urls import include, path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("quote/<int:page>", views.main, name="root_paginate"),
    path(
        "tag/<str:tag_name>/page/<int:page>/", views.quotes_by_tag, name="quotes_by_tag"
    ),
    path("author/<slug:author_slug>/", views.author_page, name="author_page"),
    path("users/", include("users.urls")),
    path("add_author/", views.add_author, name="add_author"),
    path("add_quote/", views.add_quote, name="add_quote"),
    path("scrape_quotes/", views.scrape_quotes, name="scrape_quotes"),
    path("fill_base/", views.fill_base, name="fill_base"),
    path('search/', views.searched_results, name='searched_results'),
    path('search/page/<str:query>/<int:page>/', views.searched_results, name='searched_results_paginated')

]