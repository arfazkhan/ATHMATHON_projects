from django.contrib import admin
from .models import * 

admin.site.register(BlogPost)
admin.site.register(TravelPlanTrip)
admin.site.register(FriendRequest)
admin.site.register(TripRequest)
admin.site.register(PersonalTravelRequest)
admin.site.register(Notification)

admin.site.register(Suggestion)
admin.site.register(NewsAnnouncements)
