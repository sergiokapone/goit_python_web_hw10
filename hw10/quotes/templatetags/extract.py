# from bson import ObjectId
# from django import template
# from ..utils import get_mongodb

# register = template.Library()


# def get_author(id_):
#     db = get_mongodb()
#     author = db.authors.find_one({'_id': ObjectId(id_)})
#     return author['fullname']


# register.filter('author', get_author)


from django import template
from ..models import Author, Quote
register = template.Library()


def get_author(id_):
        author = Author.objects.get(pk=id_)
        return author.fullname

def get_quotes():
        quotes = Quote.objects.all()
        return quotes


