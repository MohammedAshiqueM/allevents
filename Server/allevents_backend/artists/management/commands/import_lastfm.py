import time
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from artists.models import Artists, Genre, ArtistGenre
import os
from .artist_images import download_wikipedia_image
from django.conf import settings

LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
LASTFM_API_URL = "http://ws.audioscrobbler.com/2.0/"
SLEEP_TIME = 0.25

class Command(BaseCommand):
    help = 'Import artists from Last.fm API'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=1000)
        parser.add_argument('--offset', type=int, default=0)
        parser.add_argument('--download-images', action='store_true')

    def handle(self, *args, **options):
        limit = options['limit']
        offset = options['offset']
        download_images = options['download_images']
        batch_size = 50
        
        artists_created = 0
        errors = 0
        
        for batch_offset in range(offset, offset + limit, batch_size):
            batch_limit = min(batch_size, offset + limit - batch_offset)
            page = (batch_offset // batch_size) + 1
            
            try:
                params = {
                    'method': 'chart.gettopartists',
                    'api_key': LASTFM_API_KEY,
                    'format': 'json',
                    'limit': batch_limit,
                    'page': page
                }
                
                response = requests.get(LASTFM_API_URL, params=params)
                data = response.json()
                
                if 'artists' in data and 'artist' in data['artists']:
                    for artist_data in data['artists']['artist']:
                        try:
                            with transaction.atomic():
                                self._process_artist(artist_data, download_images)
                                artists_created += 1
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"Error processing artist: {str(e)}"))
                            errors += 1
                
                time.sleep(SLEEP_TIME)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fetching batch: {str(e)}"))
                errors += 1
                time.sleep(SLEEP_TIME * 4)
        
        self.stdout.write(self.style.SUCCESS(f"Last.fm import completed. Created {artists_created} artists with {errors} errors."))
    
    def _process_artist(self, artist_data, download_images):
        name = artist_data.get('name', '').strip()
        mbid = artist_data.get('mbid', '')
        
        if not name:
            return None
        
        if mbid:
            artist, created = Artists.objects.update_or_create(
                mbid=mbid,
                defaults={
                    'name': name,
                    'search_name': name.lower(),
                    'lastfm_name': name,
                }
            )
        else:
            artist, created = Artists.objects.update_or_create(
                lastfm_name=name,
                defaults={
                    'name': name,
                    'search_name': name.lower(),
                }
            )
        
        if 'tags' in artist_data and 'tag' in artist_data['tags']:
            for tag in artist_data['tags']['tag']:
                genre_name = tag['name'].strip().lower()
                genre, _ = Genre.objects.get_or_create(name=genre_name)
                ArtistGenre.objects.get_or_create(artist=artist, genre=genre)
        
        if download_images and not artist.profile_url:
            image_path, _ = download_wikipedia_image(artist.search_name)
            if image_path:
                artist.profile_url = os.path.join(settings.MEDIA_URL, image_path)
                artist.save()
                self.stdout.write(f"Updated profile URL for {artist.name}")
        
        artist.save()
        return artist