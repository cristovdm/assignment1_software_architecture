# myapp/forms.py
from django import forms
from .models import Author, Book

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'date_of_birth', 'country_of_origin', 'description']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'summary', 'date_of_publication', 'number_of_sales', 'author']
        widgets = {
            'date_of_publication': forms.DateInput(attrs={'type': 'date'}),
        }

