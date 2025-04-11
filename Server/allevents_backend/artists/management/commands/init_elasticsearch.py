from django.core.management.base import BaseCommand
from django_elasticsearch_dsl.registries import registry
import time
import requests
from elasticsearch.exceptions import ConnectionError as ESConnectionError

class Command(BaseCommand):
    help = 'Initialize Elasticsearch index with retry mechanism'

    def add_arguments(self, parser):
        parser.add_argument(
            '--wait',
            action='store_true',
            help='Wait for Elasticsearch to become available',
        )

    def handle(self, *args, **options):
        max_retries = 10
        retry_interval = 5 
        
        if options['wait']:
            self.stdout.write('Waiting for Elasticsearch to be ready...')
            
            for i in range(max_retries):
                try:
                    response = requests.get('http://elasticsearch:9200')
                    if response.status_code == 200:
                        self.stdout.write(self.style.SUCCESS('Elasticsearch is ready!'))
                        break
                except requests.exceptions.ConnectionError:
                    self.stdout.write(f'Elasticsearch not ready yet. Retrying in {retry_interval} seconds...')
                    time.sleep(retry_interval)
            else:
                self.stdout.write(self.style.ERROR('Could not connect to Elasticsearch after maximum retries.'))
                return
            
        # Delete existing indices
        self.stdout.write('Rebuilding Elasticsearch index...')
        try:
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
            
            self.stdout.write(self.style.SUCCESS('Successfully initialized Elasticsearch index'))
        
        except ESConnectionError:
            self.stdout.write(self.style.ERROR('Could not connect to Elasticsearch. Is it running?'))