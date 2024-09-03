from elasticsearch_dsl import Document, Text
from myapp.elasticsearch_utils import get_elasticsearch_connection

es = get_elasticsearch_connection()

class BookDocument(Document):
    summary = Text()

    class Index:
        name = 'books'

    def save(self, **kwargs):
        self.meta.id = self.meta.id or self.id
        return super().save(using=es, **kwargs)