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




"""
class AuthorListView(ListView):
    model = Author
    template_name = 'author_list.html'

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'myapp/author_detail.html'

class AuthorCreateView(CreateView):
    model = Author
    template_name = 'myapp/author_form.html'
    fields = ['name', 'date_of_birth', 'country_of_origin', 'short_description']

class AuthorUpdateView(UpdateView):
    model = Author
    template_name = 'myapp/author_form.html'
    fields = ['name', 'date_of_birth', 'country_of_origin', 'short_description']

class AuthorDeleteView(DeleteView):
    model = Author
    template_name = 'myapp/author_confirm_delete.html'
    success_url = reverse_lazy('author_list')
"""

# Repite para Book, Review y Sale
class BookListView(ListView):
    model = Book
    template_name = 'myapp/book_list.html'

class BookDetailView(DetailView):
    model = Book
    template_name = 'myapp/book_detail.html'

class BookCreateView(CreateView):
    model = Book
    template_name = 'myapp/book_form.html'
    fields = ['name', 'summary', 'date_of_publication', 'number_of_sales', 'author']

class BookUpdateView(UpdateView):
    model = Book
    template_name = 'myapp/book_form.html'
    fields = ['name', 'summary', 'date_of_publication', 'number_of_sales', 'author']

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'myapp/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')

class ReviewListView(ListView):
    model = Review
    template_name = 'myapp/review_list.html'

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'myapp/review_detail.html'

class ReviewCreateView(CreateView):
    model = Review
    template_name = 'myapp/review_form.html'
    fields = ['book', 'review', 'score', 'number_of_upvotes']

class ReviewUpdateView(UpdateView):
    model = Review
    template_name = 'myapp/review_form.html'
    fields = ['book', 'review', 'score', 'number_of_upvotes']

class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'myapp/review_confirm_delete.html'
    success_url = reverse_lazy('review_list')

class SaleListView(ListView):
    model = Sale
    template_name = 'myapp/sale_list.html'

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'myapp/sale_detail.html'

class SaleCreateView(CreateView):
    model = Sale
    template_name = 'myapp/sale_form.html'
    fields = ['book', 'year', 'sales']

class SaleUpdateView(UpdateView):
    model = Sale
    template_name = 'myapp/sale_form.html'
    fields = ['book', 'year', 'sales']

class SaleDeleteView(DeleteView):
    model = Sale
    template_name = 'myapp/sale_confirm_delete.html'
    success_url = reverse_lazy('sale_list')
