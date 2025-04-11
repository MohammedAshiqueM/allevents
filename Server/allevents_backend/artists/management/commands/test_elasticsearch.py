from django.core.management.base import BaseCommand
from artists.elasticsearch_service import ElasticsearchArtistService

class Command(BaseCommand):
    help = 'Test Elasticsearch search functionality'

    def add_arguments(self, parser):
        parser.add_argument('query', type=str, help='Search query to test')

    def handle(self, *args, **options):
        query = options['query']
        self.stdout.write(f'Testing search for: "{query}"')
        
        try:
            results = ElasticsearchArtistService.get_artist_suggestions(query, limit=10)
            
            if results:
                self.stdout.write(self.style.SUCCESS(f'Found {len(results)} results:'))
                for i, result in enumerate(results, 1):
                    self.stdout.write(f"{i}. {result['name']} (Score: {result['score']:.2f})")
            else:
                self.stdout.write('No results found.')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))