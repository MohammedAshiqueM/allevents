from django.core.management.base import BaseCommand
from django_elasticsearch_dsl.registries import registry

class Command(BaseCommand):
    help='rebulds the elastic search index'
    
    def handle(self, *args, **options):
        self.stdout.write('Rebuilding Elasticsearch index...')
        
        for index in registry.get_indices():
            index.delete(ignore=404)
            self.stdout.write(f'Deleted index: {index._name}')
        
        for index in registry.get_indices():
            index.create()
            self.stdout.write(f'Created index: {index._name}')
        
        for doc in registry.get_documents():
            qs = doc().get_queryset()
            self.stdout.write(f'Indexing {qs.count()} {doc._doc_type.name} documents...')
            doc().update(qs)
        
        self.stdout.write(self.style.SUCCESS('Successfully rebuilt Elasticsearch index'))