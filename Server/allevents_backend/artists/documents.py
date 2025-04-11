from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .es_connector import get_client
from .models import Artists

registry.connection = get_client()

@registry.register_document
class ArtistDocument(Document):
    name = fields.TextField()
    search_name = fields.TextField()
    lastfm_name = fields.TextField()
    location = fields.TextField()
    
    name_phonetic = fields.TextField(
        attr='name',
        analyzer='phonetic_analyzer'
    )
    
    aliases = fields.TextField(
        multi=True,
        # null=True
    )
    
    class Index:
        name = 'artists'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'analysis': {
                'analyzer': {
                    'phonetic_analyzer': {
                        'tokenizer': 'standard',
                        'filter': ['lowercase', 'asciifolding', 'phonetic_filter']
                    }
                },
                'filter': {
                    'phonetic_filter': {
                        'type': 'phonetic',
                        'encoder': 'double_metaphone',
                        'replace': False
                    }
                }
            }
        }
    
    class Django:
        model = Artists
        fields = [
            'id',
            'mbid',
            'profile_url',
        ]
        
        #to include relationships like genres
        related_models = []
    
    def get_instances_from_related(self, related_instance):
        #to handle related models
        return []
        
    def prepare_aliases(self, instance):
        """Prepare aliases including common abbreviations"""
        aliases = instance.aliases if hasattr(instance, 'aliases') and instance.aliases else []
        
        name_parts = instance.name.split()
        if len(name_parts) > 1:
            initials = ''.join(part[0] for part in name_parts if part)
            if len(initials) > 1:
                aliases.append(initials)
        
        return aliases