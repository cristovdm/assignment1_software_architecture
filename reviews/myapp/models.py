from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .documents import BookDocument
from .elasticsearch_utils import get_elasticsearch_connection, initialize_elasticsearch_connection

class Author(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    country_of_origin = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='authors/', null=True, blank=True)  # Nuevo campo para imagen

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=100)
    summary = models.TextField()
    date_of_publication = models.DateField()
    number_of_sales = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='books/', null=True, blank=True)  # Nuevo campo para imagen
    indexed = models.BooleanField(default=False, null=True, blank=True)
    
    def __str__(self):
        return self.name

    def get_year_of_publishing(self):
        return self.date_of_publication.year


@receiver(post_save, sender=Book)
def index_book(sender, instance, created, **kwargs):
    if instance.indexed: 
        return
    if not created:
        return

    es = get_elasticsearch_connection() 
    if not es:
        for i in range(3):
            initialize_elasticsearch_connection() 
            es = get_elasticsearch_connection()
            if es:
                break   
    if es:
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
    else:
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
