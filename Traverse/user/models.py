from django.db import models
from django.contrib.auth.models import User

    
class Vibes(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=255)
    value = models.FloatField()
    
    def __str__(self) -> str:
        return self.review


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    native_place = models.CharField(max_length=50, blank=True, null=True)
    is_online = models.BooleanField(null=True)
    vibes = models.ManyToManyField(Vibes, blank=True, related_name='vibes')
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    number = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_onTrip = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    personal_favorite_trip_blog = models.TextField(blank=True, null=True)
    location_longi = models.CharField(max_length=50, blank=True, null=True)
    location_latit = models.CharField(max_length=50, blank=True, null=True)
    friends = models.ManyToManyField(User,related_name = 'friends', blank=True)

    reviews = models.ManyToManyField(Review, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'


    def get_profile(user):
        return Profile.objects.get(user=user)