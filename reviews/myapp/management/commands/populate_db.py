# myapp/management/commands/populate_db.py
from django.core.management.base import BaseCommand
from myapp.models import Author, Book, Review, Sale
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Authors
        for _ in range(50):
            author = Author.objects.create(
                name=fake.name(),
                date_of_birth=fake.date_of_birth(),
                country_of_origin=fake.country(),
                description=fake.text()
            )

        # Create Books
        for _ in range(300):
            authors = Author.objects.all()
            book = Book.objects.create(
                name=fake.sentence(nb_words=3),
                summary=fake.text(),
                date_of_publication=fake.date(),
                number_of_sales=random.randint(0, 10000),
                author=random.choice(authors)
            )

        # Create Reviews
        books = Book.objects.all()
        for book in books:
            for _ in range(random.randint(1, 10)):
                Review.objects.create(
                    book=book,
                    review=fake.text(),
                    score=random.randint(1, 5),
                    number_of_upvotes=random.randint(0, 1000)
                )

        # Create Sales
        for book in books:
            for year in range(2018, 2023):  # Adjust the range as needed
                Sale.objects.create(
                    book=book,
                    year=year,
                    sales=random.randint(0, 5000)
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))