# myapp/forms.py
from django import forms
from .models import Author, Book, Review, Sale

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'date_of_birth', 'country_of_origin', 'description', 'image']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'summary', 'date_of_publication', 'number_of_sales', 'author', 'cover_image']
        widgets = {
            'date_of_publication': forms.DateInput(attrs={'type': 'date'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['book', 'review', 'score', 'number_of_upvotes']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['book', 'year', 'sales']

class SearchForm(forms.Form):
    search_string = forms.CharField(max_length=255, required=True, label='Search Books')