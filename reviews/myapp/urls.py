from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author_create'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author_delete'),
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author_update'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/create/', views.BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),

    path('reviews/', views.ReviewListView.as_view(), name='review_list'),
    path('reviews/create/', views.ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('reviews/<int:pk>/update/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),

    path('sales/', views.SaleListView.as_view(), name='sale_list'),
    path('sales/create/', views.SaleCreateView.as_view(), name='sale_create'),
    path('sales/<int:pk>/', views.SaleDetailView.as_view(), name='sale_detail'),
    path('sales/<int:pk>/update/', views.SaleUpdateView.as_view(), name='sale_update'),
    path('sales/<int:pk>/delete/', views.SaleDeleteView.as_view(), name='sale_delete'),
    path('sales/statistics/', views.sale_statistics, name='sale_statistics'),

    path('author_statistics/', views.author_statistics, name='author_statistics'),
    path('top_rated_books/', views.top_rated_books, name='author_statistics'),
]