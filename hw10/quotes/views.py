import json
import os
from django.http import HttpResponseNotFound

from django.shortcuts import redirect, render
from django.db.models import Count, Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic import ListView


from .forms import AuthorForm, QuoteForm
from .models import Author, Quote, Tag


class DataMixin:

    model = Quote
    paginate_by = 10
    template_name = "quotes/index.html"
    context_object_name = "quotes"

    def get_top_tags(self):
        top_tags = Tag.objects.annotate(num_quotes=Count("quote")).order_by(
            "-num_quotes"
        )[:10]
        top_tags = [(tag, 2.75 * tag.num_quotes) for tag in top_tags]
        return top_tags

    def get_quotes(self, **kwargs):

        context = kwargs

        functional_menu = [
            {"title": "About", "url_name": "quotes:about"},
            {"title": "Add Author", "url_name": "quotes:add_author"},
            {"title": "Add Quote", "url_name": "quotes:add_quote"},
            {"title": "Scrape Quotes", "url_name": "quotes:scrape_quotes"},
        ]

        top_tags = self.get_top_tags()

        if not self.request.user.is_authenticated:
            functional_menu = [functional_menu[0]]

        context["top_tags"] = top_tags
        context["functional_menu"] = functional_menu
        return context


def pageNotFound(request, exceprion):
    return HttpResponseNotFound("<h2>Page not found</h2>")


class Main(DataMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_quotes())
        return context


class SearchedResults(DataMixin, ListView):
    def get_queryset(self):
        query = self.request.GET.get("search_query")
        queryset = (
            Quote.objects.filter(
                Q(quote__icontains=query)
                | Q(tags__name__icontains=query)
                | Q(author__fullname__icontains=query)
            ).distinct()
            if query
            else Quote.objects.filter(
                id__in=self.request.session.get("search_results", [])
            )
            or super().get_queryset().only("id")
        )

        self.request.session["search_results"] = list(
            queryset.values_list("id", flat=True)
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search_query")
        context.update(self.get_quotes())
        return context


class QuotesByTag(DataMixin, ListView):
    def get_queryset(self):
        tag_name = self.kwargs["tag_name"]
        tag = Tag.objects.get(name=tag_name)
        queryset = Quote.objects.filter(tags=tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_quotes())
        return context


def author_page(request, author_slug):
    author = Author.objects.get(slug=author_slug)
    quotes = author.quote_set.all()
    print(quotes)

    context = {"author": author, "quotes": quotes}
    return render(request, "quotes/author_page.html", context)


class AddAuthorView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = "quotes/add_author.html"
    success_url = reverse_lazy("quotes:add_quote")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        author_slug = self.request.GET.get("author_slug")
        if author_slug:
            author = Author.objects.get(slug=author_slug)
            kwargs["instance"] = author
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        return response


class AddQuoteView(LoginRequiredMixin, CreateView):
    model = Quote
    form_class = QuoteForm
    template_name = "quotes/add_quote.html"
    success_url = "quotes:root"

    def form_valid(self, form):
        response = super().form_valid(form)
        quote = form.save(commit=False)
        quote.save()
        tag_name = form.cleaned_data["tags"]
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        quote.tags.add(tag)
        return response


def scrape_quotes(request):
    if request.method == "GET":
        quotes = Quote.objects.all().values("quote", "author__fullname", "tags__name")
        authors = Author.objects.all().values(
            "fullname", "born_date", "born_location", "description"
        )

        quotes_data = list(quotes)
        authors_data = list(authors)

        quotes_json = json.dumps(quotes_data, ensure_ascii=False)
        authors_json = json.dumps(authors_data, ensure_ascii=False)

        if request.GET.get("save_path"):
            save_path = request.GET.get("save_path")
            if not os.path.isdir(save_path):
                messages.error(request, "Invalid directory.")
            else:
                quotes_file_path = os.path.join(save_path, "quotes.json")
                authors_file_path = os.path.join(save_path, "authors.json")

                with open(quotes_file_path, "w", encoding="utf-8") as quotes_file:
                    quotes_file.write(quotes_json)

                with open(authors_file_path, "w", encoding="utf-8") as authors_file:
                    authors_file.write(authors_json)

                messages.success(request, "JSON files saved successfully.")
                return redirect("quotes:root")

        return render(request, "quotes/scrape_quotes.html")
