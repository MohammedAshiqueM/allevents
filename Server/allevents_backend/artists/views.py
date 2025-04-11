from rest_framework.views import APIView 
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .elasticsearch_service import ElasticsearchArtistService
from .models import Artists,Genre,ArtistGenre
from .serializers import ArtistsSerializer



class ArtistView(APIView):
    
    def get(self, request):
        artists = Artists.objects.all()
        serializer = ArtistsSerializer(artists,many=True)
        return Response(serializer.data)
    
def search_artists(request):
    query = request.GET.get('q','')
    limit = int(request.GET.get('limit',10))
    print("query", query )
    suggestions = ElasticsearchArtistService.get_artist_suggestions(query,limit)
    print("sugge",suggestions)
    return JsonResponse({
        'query':query,
        'suggestions':suggestions
    })
        
def artist_details(request, pk):
    data = get_object_or_404(Artists,pk=pk)
    serializer = ArtistsSerializer(data)
    return JsonResponse({
        'data':serializer.data
    })
        

    



