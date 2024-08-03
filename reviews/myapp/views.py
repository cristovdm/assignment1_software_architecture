from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Author, Book, Review, Sale
from django.urls import reverse_lazy
from .forms import AuthorForm

def home(request):
    return render(request, 'home.html')

# Authors CRUD
class AuthorListView(ListView):
    model = Author
    template_name = 'author_list.html'

class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'author_form.html'
    success_url = reverse_lazy('author_list')

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'

class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'author_form.html'
    success_url = reverse_lazy('author_list')

class AuthorDeleteView(DeleteView):
    model = Author
    template_name = 'author_confirm_delete.html'
    success_url = reverse_lazy('author_list')

# Books CRUD (Por el momento solo tiene la Lista)
class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'

# Reviews CRUD (Por el momento solo tiene la Lista)
class ReviewListView(ListView):
    model = Review
    template_name = 'review_list.html'


# Sales CRUD (Por el momento solo tiene la Lista)
class SaleListView(ListView):
    model = Sale
    template_name = 'sale_list.html'

