from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .documents import BookDocument

class Author(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    country_of_origin = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=100)
    summary = models.TextField()
    date_of_publication = models.DateField()
    number_of_sales = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    indexed = models.BooleanField(default=False)  # Nuevo campo para rastrear la indexación

    def __str__(self):
        return self.name

    def get_year_of_publishing(self):
        return self.date_of_publication.year

@receiver(post_save, sender=Book)
def index_book(sender, instance, **kwargs):
    try:
        book_document = BookDocument(
            meta={'id': instance.id},
            summary=instance.summary
        )
        book_document.save()
        instance.indexed = True 
        instance.save(update_fields=['indexed'])
        print(f"Libro indexado: {instance.name}")
    except Exception as e:
        print(f"Error al indexar {instance.name}: {str(e)}")
        instance.indexed = False 
        instance.save(update_fields=['indexed']) 


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True)
    review = models.TextField()
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    number_of_upvotes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Review with score {self.score}"

class Sale(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    year = models.IntegerField()
    sales = models.IntegerField()

    def __str__(self):
        return f"{self.book.name} - {self.year}"
