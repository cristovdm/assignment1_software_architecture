from .models import Book
from .documents import BookDocument

def reindex_books():
    # Buscar todos los libros que no han sido indexados
    books_to_reindex = Book.objects.filter(indexed=False)

    for book in books_to_reindex:
        try:
            book_document = BookDocument(
                meta={'id': book.id},
                summary=book.summary
            )
            book_document.save()
            book.indexed = True  # Marcar como indexado
            book.save(update_fields=['indexed'])  # Actualizar el estado del libro
        except Exception as e:
            print(f"Error al reindexar {book.name}: {str(e)}")