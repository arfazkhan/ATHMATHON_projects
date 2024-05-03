from django.db import models
from django.contrib.auth.models import User
import uuid

from user.models import Vibes



class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='suggestion_images/', null=True, blank=True)
    vibes = models.ManyToManyField(Vibes, blank=True)
    desc = models.CharField(max_length=255)
    place_name = models.CharField(max_length=255)

    def __str__(self):
        return self.place_name

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_users')

    def __str__(self):
        return self.title


class TravelPlanTrip(models.Model):
    JOIN = 'join'
    CREATE = 'create'
    JOIN_OR_CREATE_GROUP_CHOICES = [
        (JOIN, 'Join'),
        (CREATE, 'Create'),
    ]
    join_or_create_group = models.CharField(
        max_length=6,
        choices=JOIN_OR_CREATE_GROUP_CHOICES,
        default=JOIN,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    place_name = models.CharField(max_length=100, null=True)
    longitude = models.CharField(max_length=100, default=0)
    latitude = models.CharField(max_length=100, default=0)
    mode_of_travel = models.CharField(max_length=20, null=True)
    start_travel_date = models.DateField()
    end_travel_date = models.DateField()
    travel_vibe = models.TextField(blank=True, null=True)
    share_facilities = models.CharField(max_length=20, default=False, blank=True, null=True, choices=[('no', 'No'), ('yes', 'Yes')])
    share_every_facility = models.CharField(max_length=20, blank=True, null=True,  choices=[('no', 'No'), ('yes', 'Yes')])
    facilities = models.CharField(max_length=255, blank=True, null=True)
    facilities_image = models.ImageField(
        upload_to='facilities/', blank=True, null=True)

    group_name = models.UUIDField(default=uuid.uuid4)
    group_users = models.ManyToManyField("auth.User", verbose_name=(
        "group"), related_name='group_users', null=True, blank=True)
    group_facilities_share = models.CharField(
        max_length=100, blank=True, null=True)

    def __str__(self):
        return " To " + self.place_name


class Chat(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_chats')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_chats')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username + " -> " + self.receiver.username


class GroupChat(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        TravelPlanTrip, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username + " -> " + self.receiver.place_name


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name='friend_requests_received', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Friend Request from {self.from_user} to {self.to_user}'


class PersonalTravelRequest(models.Model):
    from_user = models.ForeignKey(
        User, related_name='personel_travel_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name='personel_travel_requests_received', on_delete=models.CASCADE)
    trip = models.ForeignKey(
        TravelPlanTrip, related_name='personel_travel_requests_received', on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Personal Travel Request from {self.from_user} to {self.to_user}'


class TripRequest(models.Model):
    from_user = models.ForeignKey(
        User, related_name='trip_requests_sent', on_delete=models.CASCADE)
    to_trip = models.ForeignKey(
        TravelPlanTrip, related_name='trip_requests_received', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def accept(self):
        self.accepted = True
        self.save()

    def __str__(self):
        return f'Trip Request from {self.from_user} {self.to_trip}'


class Notification(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications_sent')
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications_received')
    trip = models.ForeignKey(
        TravelPlanTrip, on_delete=models.CASCADE, related_name='trip_notifications_received', null=True, blank=True)
    message = models.CharField(max_length=255)

    def __str__(self):
        return self.from_user.username + " -----> " + self.to_user.username



class NewsAnnouncements(models.Model):
    news = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    icon = models.CharField(max_length=255, blank=True, null=True, default='bell')
    date = models.DateField(auto_now_add=True)
    
    
    def __str__(self):
        return self.news
    