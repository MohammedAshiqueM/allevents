import time
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from artists.models import Artists, Genre, ArtistGenre
import musicbrainzngs
import os
from django.conf import settings
from .artist_images import download_wikipedia_image

class Command(BaseCommand):
    help = 'Import artists from MusicBrainz API'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=1000)
        parser.add_argument('--offset', type=int, default=0)
        parser.add_argument('--download-images', action='store_true')

    def handle(self, *args, **options):
        
        musicbrainzngs.set_useragent(
            "allevents", "0.1", os.getenv('MUSICBRAINZ_ACC_EMAIL')
        )
        
        limit = options['limit']
        offset = options['offset']
        print("offset",offset)
        
        download_images = options['download_images']
        batch_size = 100
        
        self.stdout.write(f"Importing {limit} artists from offset {offset}")
        artists_created = 0
        errors = 0
        
        for batch_offset in range(offset, offset + limit, batch_size):
            batch_limit = min(batch_size, offset + limit - batch_offset)
            
            try:
                result = musicbrainzngs.search_artists(
                    limit=batch_limit,
                    offset=batch_offset,
                    query="type:Person OR type:Group"
                )
                
                for artist_data in result['artist-list']:
                    try:
                        with transaction.atomic():
                            self._process_artist(artist_data, download_images)
                            artists_created += 1
                    except Exception as e:
                        self.stdout.write(f"Error processing artist: {str(e)}")
                        errors += 1
                
                time.sleep(1.1)
                
            except Exception as e:
                self.stdout.write(f"Error fetching batch: {str(e)}")
                errors += 1
                time.sleep(2.2)
        
        self.stdout.write(f"Import completed. Created {artists_created} artists with {errors} errors.")
    
    def _process_artist(self, artist_data, download_images):
        mbid = artist_data.get('id')
        name = artist_data.get('name', '').strip()
        
        if not name:
            return None
            
        artist, created = Artists.objects.update_or_create(
            mbid=mbid,
            defaults={
                'name': name,
                'search_name': name.lower(),
                'lastfm_name': name,
            }
        )
        
        if 'area' in artist_data and artist_data['area']:
            artist.location = artist_data['area'].get('name', '')
        
        if 'tag-list' in artist_data:
            for tag in artist_data['tag-list']:
                if 'name' in tag and tag['name'] and int(tag['count']) > 1:
                    genre_name = tag['name'].strip().lower()
                    genre, _ = Genre.objects.get_or_create(name=genre_name)
                    ArtistGenre.objects.get_or_create(artist=artist, genre=genre)
        
        # Download profile image
        if download_images and not artist.profile_url:
            image_path, _ = download_wikipedia_image(artist.search_name)
            if image_path:
                artist.profile_url = os.path.join(settings.MEDIA_URL, image_path)
                artist.save()
                self.stdout.write(f"Updated profile URL for {artist.name}")
        
        artist.save()
        return artist