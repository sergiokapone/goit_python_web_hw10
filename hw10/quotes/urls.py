from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.Main.as_view(), name="root"),
    path(
        "about/", TemplateView.as_view(template_name="quotes/about.html"), name="about"
    ),
    path("tag/<str:tag_name>/", views.QuotesByTag.as_view(), name="quotes_by_tag"),
    path("author/<slug:author_slug>/", views.author_page, name="author_page"),
    path("users/", include("users.urls")),
    path("scrape_quotes/", views.scrape_quotes, name="scrape_quotes"),
    path("search/", views.SearchedResults.as_view(), name="searched_results"),
    path("add_author/", views.AddAuthorView.as_view(), name="add_author"),
    path("add_quote/", views.AddQuoteView.as_view(), name="add_quote"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
