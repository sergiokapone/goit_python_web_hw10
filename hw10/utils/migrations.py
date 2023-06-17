import os
import django
from django.utils.text import slugify

# from pymongo import MongoClient

if "DJANGO_SETTINGS_MODULE" in os.environ:
    del os.environ["DJANGO_SETTINGS_MODULE"]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw10.settings")
django.setup()


from quotes.models import Author # noqa




authors = Author.objects.all()


for author in authors:
    author.slug = slugify(author.fullname)
    author.save()