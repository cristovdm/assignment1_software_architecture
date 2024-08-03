from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author_create'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author_delete'),
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author_update'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    

    path('books/', views.BookListView.as_view(), name='book_list'),

    path('reviews/', views.ReviewListView.as_view(), name='review_list'),

    path('sales/', views.SaleListView.as_view(), name='sale_list'),


    # Las de abajo todavía no son implementadas.

    path('books/<int:pk>/', views.BookListView.as_view(), name='book_detail'),
    path('books/create/', views.BookListView.as_view(), name='book_create'),
    path('books/<int:pk>/update/', views.BookListView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', views.BookListView.as_view(), name='book_delete'),

    
    path('reviews/<int:pk>/', views.BookListView.as_view(), name='review_detail'),
    path('reviews/create/', views.BookListView.as_view(), name='review_create'),
    path('reviews/<int:pk>/update/', views.BookListView.as_view(), name='review_update'),
    path('reviews/<int:pk>/delete/', views.BookListView.as_view(), name='review_delete'),

    path('sales/', views.BookListView.as_view(), name='sale_list'),
    path('sales/<int:pk>/', views.BookListView.as_view(), name='sale_detail'),
    path('sales/create/', views.BookListView.as_view(), name='sale_create'),
    path('sales/<int:pk>/update/', views.BookListView.as_view(), name='sale_update'),
    path('sales/<int:pk>/delete/', views.BookListView.as_view(), name='sale_delete'),
]