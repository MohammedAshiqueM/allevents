
from django.urls import path
from .views import ArtistView,search_artists,artist_details

urlpatterns = [
    path('', ArtistView.as_view(), name="artists" ),
    path('search/', search_artists, name="search" ),
    path('<int:pk>/', artist_details, name="details" ),
    
]
