# myapp/forms.py
from django import forms
from .models import Author

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'date_of_birth', 'country_of_origin', 'description']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
