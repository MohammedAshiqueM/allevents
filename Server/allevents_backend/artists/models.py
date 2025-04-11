from django.db import models

class Artists(models.Model):
    name = models.CharField(max_length=255)
    search_name = models.CharField(max_length=255)
    mbid = models.CharField(max_length=50,blank=True,unique=True,null=True)
    lastfm_name = models.CharField(max_length=255,blank=True,unique=True,null=True)
    location = models.CharField(max_length=255,blank=True)
    profile_url = models.CharField(max_length=500,blank=True)
    gentre = models.ManyToManyField('Genre',through='ArtistGenre')
    
    def __str__(self):
        return self.name

    class Meta:
        indexes=[
            models.Index(fields=['search_name']),
            models.Index(fields=['lastfm_name'])
        ]    

class Genre(models.Model):
    name = models.CharField(max_length=100,unique=True)
    
    
class ArtistGenre(models.Model):
    artist = models.ForeignKey(Artists,on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre,on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('artist','genre')