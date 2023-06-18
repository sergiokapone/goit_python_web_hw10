from django import forms
from .models import Author, Quote

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(forms.ModelForm):

    author_choices = Author.objects.all()

    tags = forms.CharField(label='Tags', required=False)  # Заменяем поле на CharField


    author = forms.ModelChoiceField(
        label='Author',
        queryset=author_choices,
        to_field_name='fullname',
        empty_label=None
    )

    class Meta:
        model = Quote
        fields = ['quote', 'tags', 'author']



    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['author'].choices = [(author.id, author.fullname) for author in Author.objects.all()]
