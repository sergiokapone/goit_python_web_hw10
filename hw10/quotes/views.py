from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.db.models import Count

from .forms import AuthorForm, QuoteForm
from .models import Author, Quote, Tag
from django.contrib.auth.decorators import login_required
from django.contrib import messages




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

    return render(
        request,
        "quotes/index.html",
        context={"quotes": quotes_on_page, "top_tags": top_tags},
    )


def quotes_by_tag(request, tag_name, page=1):
    tag = Tag.objects.get(name=tag_name)
    quotes = Quote.objects.filter(tags=tag)

    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)

    top_tags = get_top_tags()

    return render(
        request,
        "quotes/quotes_by_tag.html",
        context={"quotes": quotes_on_page, "tag": tag, "top_tags": top_tags},
    )


def author_page(request, author_slug):
    author = Author.objects.get(slug=author_slug)

    top_tags = get_top_tags()

    return render(
        request,
        "quotes/author_page.html",
        context={"author": author, "top_tags": top_tags},
    )


@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullname']
            if not Author.objects.filter(fullname=fullname).exists():
                form.save()
                return redirect('quotes:root')
            else:
                messages.error(request, 'Author already exists.')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()
            
            # Processing entered text to create a new tag
            tag_name = form.cleaned_data['tags']
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            quote.tags.add(tag)
            
            return redirect('quotes:root')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})

