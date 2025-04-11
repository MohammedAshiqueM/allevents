
from rest_framework import serializers
from .models import Artists,Genre,ArtistGenre


class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        fields = ['name']
        
    
class ArtistsSerializer(serializers.ModelSerializer):
    gentre = GenreSerializer(many=True,read_only=True)
    class Meta:
        model = Artists
        fields = ['name','gentre','location','profile_url']
        