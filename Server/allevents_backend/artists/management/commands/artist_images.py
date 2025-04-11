import os
import requests
from io import BytesIO
from PIL import Image
from django.conf import settings
import wikipediaapi

def download_wikipedia_image(search_name):
    """
    Improved Wikipedia image downloader with better error handling
    Returns: (relative_path, image_url) or (None, None)
    """
    headers = {
        'User-Agent': 'allevents/1.0 (ashiqueexample@email.com)'
    }
    
    try:
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={search_name}&format=json"
        search_response = requests.get(search_url, headers=headers, timeout=10)
        search_response.raise_for_status()
        search_data = search_response.json()
        
        if not search_data.get('query', {}).get('search'):
            print(f"No Wikipedia page found for {search_name}")
            return None, None
            
        page_title = search_data['query']['search'][0]['title']
        
        image_params = {
            'action': 'query',
            'titles': page_title,
            'prop': 'pageimages',
            'pithumbsize': 500,
            'format': 'json'
        }
        
        image_response = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params=image_params,
            headers=headers,
            timeout=10
        )
        image_response.raise_for_status()
        image_data = image_response.json()
        
        pages = image_data.get('query', {}).get('pages', {})
        image_url = None
        
        for page in pages.values():
            if 'thumbnail' in page:
                image_url = page['thumbnail']['source']
                break
                
        if not image_url:
            print(f"No image found for {search_name}")
            return None, None
            
        img_response = requests.get(image_url, headers=headers, timeout=10)
        img_response.raise_for_status()
        
        if len(img_response.content) < 1024:  # At least 1KB
            print(f"Image too small for {search_name}")
            return None, None
            
        filename = f"wiki_{search_name.lower().replace(' ', '_')}.jpg"
        relative_path = f"artist_images/{filename}"
        full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'wb') as f:
            f.write(img_response.content)
        
        print(f"Successfully downloaded image for {search_name}")
        return relative_path, image_url
        
    except Exception as e:
        print(f"Error processing {search_name}: {str(e)}")
        return None, None