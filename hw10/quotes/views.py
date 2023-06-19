import json
import os
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.db.models import Count, Q

from .forms import AuthorForm, QuoteForm
from .models import Author, Quote, Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pymongo import MongoClient


def get_top_tags():
    top_tags = Tag.objects.annotate(num_quotes=Count("quote")).order_by("-num_quotes")[
        :10
    ]
    top_tags = [(tag, 2 * tag.num_quotes) for tag in top_tags]
    return top_tags


def main(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)

    top_tags = get_top_tags()
    context={"quotes": quotes_on_page, "top_tags": top_tags}

    return render(
        request,
        "quotes/index.html",
        context,
    )


def quotes_by_tag(request, tag_name, page=1):
    tag = Tag.objects.get(name=tag_name)
    quotes = Quote.objects.filter(tags=tag)

    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)

    top_tags = get_top_tags()
    context={"quotes": quotes_on_page, "tag": tag, "top_tags": top_tags}

    return render(
        request,
        "quotes/quotes_by_tag.html",
        context,
    )


def author_page(request, author_slug):
    author = Author.objects.get(slug=author_slug)

    top_tags = get_top_tags()
    context={"author": author, "top_tags": top_tags}

    return render(
        request,
        "quotes/author_page.html",
        context,
    )


@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data["fullname"]
            if not Author.objects.filter(fullname=fullname).exists():
                form.save()
                return redirect("quotes:root")
            else:
                messages.error(request, "Author already exists.")
    else:
        form = AuthorForm()
    return render(request, "quotes/add_author.html", {"form": form})


@login_required
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()

            # Processing entered text to create a new tag
            tag_name = form.cleaned_data["tags"]
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            quote.tags.add(tag)

            return redirect("quotes:root")
    else:
        form = QuoteForm()
        context={"form": form}
    return render(request, "quotes/add_quote.html", context)


def search_results(request):
    query = request.GET.get("search_query")
    results = []
    if query:
        results = Quote.objects.filter(
            Q(quote__icontains=query)
            | Q(tags__name__icontains=query)
            | Q(author__fullname__icontains=query)
        ).distinct()

    top_tags = get_top_tags()

    context = {
        "query": query,
        "quotes": results,
        "top_tags": top_tags,
    }
    return render(request, "quotes/search_results.html", context)


def fill_base(request):
    client = MongoClient("mongodb+srv://PSM:GoIThw8@cluster0.y0zbkd4.mongodb.net/")
    db = client.Quotes

    authors = db.authors.find()
    quotes = db.quotes.find()

    for author in authors:
        Author.objects.get_or_create(
            fullname=author["fullname"],
            born_date=author["born_date"],
            born_location=author["born_location"],
            description=author["description"],
        )

    for quote in quotes:
        tags = []
        for tag in quote["tags"]:
            t, *_ = Tag.objects.get_or_create(name=tag)
            tags.append(t)

        exist_quote = bool(len(Quote.objects.filter(quote=quote["quote"])))

        if not exist_quote:
            author = db.authors.find_one({"_id": quote["author"]})
            a = Author.objects.get(fullname=author["fullname"])
            q = Quote.objects.create(quote=quote["quote"], author=a)
            for tag in tags:
                q.tags.add(tag)

    messages.success(request, "Base filled successfully!")

    return redirect("quotes:root")


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
