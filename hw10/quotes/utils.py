from django.utils.text import slugify
from .models import Author

authors = Author.objects.all()

for author in authors:
    author.slug = slugify(author.fullname)
    author.save()
