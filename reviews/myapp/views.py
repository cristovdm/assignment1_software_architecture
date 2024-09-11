from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Author, Book, Review, Sale
from django.urls import reverse_lazy
from .forms import AuthorForm, BookForm, ReviewForm, SaleForm, SearchForm
from django.db.models import Avg, Count, Sum, Max, Min
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.cache import cache
from elasticsearch_dsl import Search, Q
from .elasticsearch_utils import get_elasticsearch_connection, initialize_elasticsearch_connection
from .forms import SearchForm
from .reindex_books import reindex_books
import os

USE_ELASTICSEARCH = os.getenv('USE_ELASTICSEARCH', False)

if USE_ELASTICSEARCH == "false":
    USE_ELASTICSEARCH = False
if USE_ELASTICSEARCH == "true":
    USE_ELASTICSEARCH = True

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
    
    cache_key = '123_all_books' 
    cache_time = 60 * 15 
    
    cached_books = None
    
    def get_queryset(self):
        if cache:
            cached_books = cache.get(self.cache_key)
        
        if cached_books:
            return cached_books
        
        queryset = Book.objects.all() 
        
        if cache:
            cache.set(self.cache_key, queryset, self.cache_time)
        
        return queryset
    
class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('book_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if cache:
            cache._cache.flush_all()
        return response

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('book_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if cache:
            cache._cache.flush_all()
        return response

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if cache:
            cache._cache.flush_all()
        return response

# Reviews CRUD (Por el momento solo tiene la Lista)
class ReviewListView(ListView):
    model = Review
    template_name = 'review_list.html'

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review_list')

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'review_detail.html'

class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('review_list')

class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'
    success_url = reverse_lazy('review_list')

# Sales CRUD (Por el momento solo tiene la Lista)
class SaleListView(ListView):
    model = Sale
    template_name = 'sale_list.html'

class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale_form.html'
    success_url = reverse_lazy('sale_list')

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'sale_detail.html'

class SaleUpdateView(UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale_form.html'
    success_url = reverse_lazy('sale_list')

class SaleDeleteView(DeleteView):
    model = Sale
    template_name = 'sale_confirm_delete.html'
    success_url = reverse_lazy('sale_list')

def author_statistics(request):
    authors = Author.objects.annotate(
        num_books=Count('book'),
        avg_score=Avg('book__review__score'),
        total_sales=Sum('book__sale__sales')
    )
    return render(request, 'author_statistics.html', {'authors': authors})


def get_top_rated_books(request):
    reviews = (
        Review.objects.values('book__name')  
        .annotate(
            average_score=Avg('score'),
            count=Count('id'),
            max_upvote_review=Max('number_of_upvotes'),
            min_upvote_review=Min('number_of_upvotes'),
        )
        .order_by('-average_score')[:10]  
    )

    data = []
    for review in reviews:
        max_review = Review.objects.filter(book__name=review['book__name'], number_of_upvotes=review['max_upvote_review']).first()
        min_review = Review.objects.filter(book__name=review['book__name'], number_of_upvotes=review['min_upvote_review']).first()

        data.append({
            "book": review['book__name'],
            "average_score": review['average_score'],
            "count": review['count'],
            "max_upvote_review": (max_review.review, max_review.number_of_upvotes) if max_review else ("", 0),
            "min_upvote_review": (min_review.review, min_review.number_of_upvotes) if min_review else ("", 0),
        })

    return data


def top_rated_books(request):
    cache_key = '123_sorted_books' 
    cache_time = 86400  
    sorted_books = None
    
    if cache:
        sorted_books = cache.get(cache_key)
    
    if not sorted_books:
        sorted_books = get_top_rated_books(request)
        
        if cache:
            cache.set(cache_key, sorted_books, cache_time)

    return render(request, 'top_rated_books.html', {'sorted_books': sorted_books})

# * A table that shows the top 50 selling books of all time, 
# showing their total sales for the book, total sales 
# for the author, and if the book was the on the top 5 selling 
# books the year of its publication.
def sale_statistics(request):
    # Obtener las ventas totales por libro en la base de datos usando agregación
    total_sales_per_book = (
        Sale.objects.values('book')
        .annotate(total_sales=Sum('sales'))
        .order_by('-total_sales')[:50]  # Solo los 50 libros más vendidos
    )
    
    # Crear un diccionario para almacenar las ventas por autor
    sales_per_author = {}
    for sale in total_sales_per_book:
        book = Book.objects.get(pk=sale['book'])  # Obtener el objeto Book relacionado
        if book.author in sales_per_author:
            sales_per_author[book.author] += sale['total_sales']
        else:
            sales_per_author[book.author] = sale['total_sales']
    
    # Obtener las ventas por año para cada libro
    sales_per_year = (
        Sale.objects.values('book', 'year')
        .annotate(yearly_sales=Sum('sales'))
        .order_by('year', '-yearly_sales')
    )
    
    # Crear un diccionario para almacenar los 5 libros más vendidos por año
    top_5_selling_books_per_year = {}
    for sale in sales_per_year:
        year = sale['year']
        book = Book.objects.get(pk=sale['book'])
        if year not in top_5_selling_books_per_year:
            top_5_selling_books_per_year[year] = [(book, sale['yearly_sales'])]
        else:
            if len(top_5_selling_books_per_year[year]) < 5:
                top_5_selling_books_per_year[year].append((book, sale['yearly_sales']))

    # Preparar las estadísticas para los 50 libros más vendidos
    top50_statistics = {}
    for sale in total_sales_per_book:
        book = Book.objects.get(pk=sale['book'])  # Obtener el objeto Book relacionado
        top50_statistics[book] = [
            sale['total_sales'], 
            sales_per_author.get(book.author, 0),
        ]
        year_of_publication = book.get_year_of_publishing()
        is_top5_in_year = book in [b[0] for b in top_5_selling_books_per_year.get(year_of_publication, [])]
        top50_statistics[book].append(is_top5_in_year)

    return render(request, 'sale_statistics.html', {'sales_statistics': top50_statistics})


def search_window(request):
    return render(request, 'search_window.html', {'books_found': []})

if USE_ELASTICSEARCH:
    initialize_elasticsearch_connection()    
    
def search_books(request):
    form = SearchForm(request.POST or None)
    search_string = ""
    books = []
    books_found = []

    if USE_ELASTICSEARCH:
        es = get_elasticsearch_connection() 
        if not es:
            for i in range(3):
                initialize_elasticsearch_connection() 
                es = get_elasticsearch_connection()
                if es:
                    break   
    

    if form.is_valid():
        search_string = form.cleaned_data.get("search_string")
        search_words = search_string.split()
        
        reindex_books()

        if USE_ELASTICSEARCH:
            if es: 
                s = Search(using=es, index="books")
                
                should_clauses = []
                for word in search_words:
                    q = Q("match", summary=word)
                    should_clauses.append(q)
                
                bool_query = Q("bool", should=should_clauses, minimum_should_match=1)
        
                s = s.query(bool_query)
                response = s.execute()
                
                book_ids = [hit.meta.id for hit in response]
                
                books = Book.objects.filter(id__in=book_ids)

        else:  
            all_books = Book.objects.all()
            for word in search_words:
                books_found += all_books.filter(summary__icontains=word)
            books = list(set(books_found)) 

    paginator = Paginator(books, 10)
    page = request.GET.get('page', 1)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    return render(request, 'search_window.html', {
        'form': form, 
        'books_found': books, 
        'search_string': search_string,
        'search_words': search_string.split()
    })
