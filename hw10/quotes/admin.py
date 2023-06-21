from django.contrib import admin

from .models import Author, Tag, Quote


class QuoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'quote', 'author']
    list_display_links = ['id', 'author']
    search_fields = ('author',)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'photo']
    list_display_links = ['id', 'fullname']
    search_fields = ('fullname',)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Tag)



