from elasticsearch import Elasticsearch
from django.conf import settings

def get_client():
    """Return a properly configured Elasticsearch client for ES 8.x"""
    es_hosts = settings.ELASTICSEARCH_DSL['default']['hosts']
    
    return Elasticsearch(
        es_hosts,

    )