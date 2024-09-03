from elasticsearch_dsl import Document, Text

class BookDocument(Document):
    summary = Text()

    class Index:
        name = 'books'

    def save(self, **kwargs):
        self.meta.id = self.meta.id or self.id
        return super().save(**kwargs)
