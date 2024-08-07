from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Author, Book, Review, Sale
from django.urls import reverse_lazy
from .forms import AuthorForm, BookForm, ReviewForm, SaleForm
from django.db.models import Avg, Count, Sum

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

def top_rated_books(request):
    reviews = list(Review.objects.all())
    data = {}

    for review in reviews:
        book = review.book.name
        if book not in data:
            data[book] = {
                "average_score" : review.score, 
                "count" : 1,
                "max_upvote_review" : (review.review, review.number_of_upvotes),
                "min_upvote_review" : (review.review, review.number_of_upvotes),
                }
        else:
            data[book]["average_score"] += review.score 
            data[book]["count"] += 1

            upvotes = review.number_of_upvotes

            if upvotes > data[book]["max_upvote_review"][1]:
                data[book]["max_upvote_review"] = (review.review, review.number_of_upvotes)

            if upvotes < data[book]["min_upvote_review"][1]:
                data[book]["min_upvote_review"] = (review.review, review.number_of_upvotes)

    for book in data:
        data[book]["average_score"] /= data[book]["count"]
    
    sorted_books = sorted(data.items(), key=lambda x : x[1]["average_score"], reverse=True)
    sorted_books = sorted_books[0:10]

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
    

