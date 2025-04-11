from elasticsearch_dsl import Q as ESQ
from .documents import ArtistDocument
from elasticsearch import Elasticsearch
from django.conf import settings

class ElasticsearchArtistService:
    @staticmethod
    def get_connection():
        es_hosts = settings.ELASTICSEARCH_DSL['default']['hosts']
        return Elasticsearch(es_hosts)
    
    @staticmethod
    def search_artists(query, limit=10):
        if not query or len(query) < 2:
            return []
        
        search_query = query.lower().strip()
        
        search = ArtistDocument.search()
        
        multi_match = ESQ('multi_match', 
            query=search_query,
            fields=['name^3', 'search_name^2', 'lastfm_name', 'aliases'],
            fuzziness='AUTO'
        )
        
        prefix_match = ESQ('prefix', 
            search_name={
                'value': search_query,
                'boost': 1.5
            }
        )
        
        search = search.query(
            ESQ('bool', should=[multi_match, prefix_match])
        )
        
        results = search[:limit].execute()
        
        return results
    
    @staticmethod
    def get_artist_suggestions(query, limit=5):
        """Returns a list of artist suggestions based on the query"""
        results = ElasticsearchArtistService.search_artists(query, limit)
        
        return [{
            'id': hit.id,
            'name': hit.name,
            'score': hit.meta.score,
            'original_query': query
        } for hit in results]
        
    @staticmethod
    def rebuild_index():
        """Rebuild the Elasticsearch index"""
        ArtistDocument().init()