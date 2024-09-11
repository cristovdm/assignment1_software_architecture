from .models import Book
from .documents import BookDocument
from .elasticsearch_utils import get_elasticsearch_connection, initialize_elasticsearch_connection

def reindex_books():

    books = Book.objects.all()
    books_to_reindex = [book for book in books if book.indexed is False]

    es = get_elasticsearch_connection() 
    if not es:
        for i in range(3):
            initialize_elasticsearch_connection() 
            es = get_elasticsearch_connection()
            if es:
                break   

    for book in books_to_reindex:
        if es:
            try:
                book_document = BookDocument(
                    meta={'id': book.id},
                    summary=book.summary
                )
                book_document.save()
                book.indexed = True
                book.save(update_fields=['indexed'])
            except Exception as e:
                print(f"Error al reindexar {book.name}: {str(e)}")