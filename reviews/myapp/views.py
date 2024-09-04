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
from .documents import BookDocument
from .reindex_books import reindex_books

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

class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('book_list')

class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('book_list')

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'
    success_url = reverse_lazy('book_list')

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

    print("DATAA: ", data)
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
    all_sales = Sale.objects.all()
    total_sales_per_book = {}
    sales_per_year = {}
    sales_per_author = {}
    for sale in all_sales:
        if sale.book in total_sales_per_book:
            total_sales_per_book[sale.book] += sale.sales
        else:
            total_sales_per_book[sale.book] = sale.sales
        if sale.year in sales_per_year:
            if sale.book.name in sales_per_year[sale.year]:
                sales_per_year[sale.year][sale.book] += sale.sales
            else:
                sales_per_year[sale.year][sale.book] = sale.sales
        else:
            sales_per_year[sale.year] = {sale.book: sale.sales}
    top_5_selling_books_per_year = {}
    for year in sales_per_year:
        sorted_sales_per_book_per_year = dict(sorted(sales_per_year[year].items(), key=lambda item: item[1], reverse=True))
        for i, book in enumerate(sorted_sales_per_book_per_year):
            if i < 5:
                if year not in top_5_selling_books_per_year:
                    top_5_selling_books_per_year[year] = [book]
                else:
                    top_5_selling_books_per_year[year].append(book)          
    total_sales_per_book = dict(sorted(total_sales_per_book.items(), key=lambda item: item[1], reverse=True))
    for book in total_sales_per_book:
        if book.author in sales_per_author:
            sales_per_author[book.author] += total_sales_per_book[book]
        else:
            sales_per_author[book.author] = total_sales_per_book[book]
    top50_statistics = {}
    for i, book in enumerate(total_sales_per_book):
        if i < 50:
            top50_statistics[book] = [total_sales_per_book[book], sales_per_author[book.author]]
            year_of_publication = book.get_year_of_publishing()
            if year_of_publication in top_5_selling_books_per_year:
                if book in top_5_selling_books_per_year[year_of_publication]:
                    top50_statistics[book].append(True)
                else:
                    top50_statistics[book].append(False)
            else:
                top50_statistics[book].append(False)
    return render(request, 'sale_statistics.html', {'sales_statistics': top50_statistics})

def search_window(request):
    return render(request, 'search_window.html', {'books_found': []})

initialize_elasticsearch_connection()    
    
def search_books(request):
    form = SearchForm(request.POST or None)
    search_string = ""
    books = []
    books_found = []

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

        if es: 
            s = Search(using=es, index="books")
            for word in search_words:
                q = Q("match", summary=word)
                s = s.query(q)
            response = s.execute()
            book_ids = [hit.meta.id for hit in response]
            
            print("USANDO ELASTICSEARCH")
            
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
