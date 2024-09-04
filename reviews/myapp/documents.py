from elasticsearch_dsl import Document, Text
from myapp.elasticsearch_utils import get_elasticsearch_connection, initialize_elasticsearch_connection

es = get_elasticsearch_connection() 
if not es:
    for i in range(3):
        initialize_elasticsearch_connection() 
        es = get_elasticsearch_connection()
        if es:
            break   

class BookDocument(Document):
    summary = Text()

    class Index:
        name = 'books'

    def save(self, **kwargs):
        self.meta.id = self.meta.id or self.id
        return super().save(using=es, **kwargs)