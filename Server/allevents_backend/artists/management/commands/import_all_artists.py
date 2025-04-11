from django.core.management.base import BaseCommand
from django.core import management

class Command(BaseCommand):
    help = 'Import artists from all available APIs'
    
    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=100000, help='Maximum number of artists to import')
        parser.add_argument('--offset', type=int, default=0)
        parser.add_argument('--download-images', action='store_true', help='Download artist images')
        
    def handle(self, *args, **options):
        limit = options['limit']
        initial_offset = options['offset']
        print(initial_offset)
        download_images = options['download_images']
        
        # Distribute the limit to MusicBrainz and Last.fm
        musicbrainz_limit = min(limit, 100)  # MusicBrainz
        lastfm_limit = min(limit - musicbrainz_limit, 100)  # Last.fm
        
        # Import from MusicBrainz
        self.stdout.write(self.style.NOTICE("Starting MusicBrainz imports..."))
        batch_size = 1000
        current_offset = initial_offset
        if musicbrainz_limit > 0:
            for batch_offset in range(0, musicbrainz_limit, batch_size):
                current_batch = min(batch_size, musicbrainz_limit - batch_offset)
                self.stdout.write(f"Importing MusicBrainz batch {current_offset}-{current_offset + current_batch}...")
                
                management.call_command(
                    'import_musicbrainz',
                    limit=current_batch,
                    offset=current_offset,
                    download_images=download_images
                )
                current_offset += current_batch
        
        # Import from Last.fm
        if lastfm_limit > 0:
            self.stdout.write(self.style.NOTICE("Starting Last.fm imports..."))
            for batch_offset in range(0, lastfm_limit, batch_size):
                current_batch = min(batch_size, lastfm_limit - batch_offset)
                self.stdout.write(f"Importing Last.fm batch {current_offset}-{current_offset + current_batch}...")
                
                management.call_command(
                    'import_lastfm',
                    limit=current_batch,
                    offset=current_offset,
                    download_images=download_images
                )
                current_offset += current_batch
        
        self.stdout.write(self.style.SUCCESS("All artist imports completed!"))