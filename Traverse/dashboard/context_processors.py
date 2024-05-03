from dashboard.models import NewsAnnouncements, TravelPlanTrip
from django.utils import timezone
from geopy import distance
from user.models import Profile

def updating_loc(request):
    if request.user.is_authenticated:
        my_trip = TravelPlanTrip.objects.filter(user=request.user).first()
        if Profile.objects.get(user=request.user).location_latit and Profile.objects.get(user=request.user).location_longi:
            user_profile = Profile.objects.get(user=request.user)
            center_point = (user_profile.location_longi, user_profile.location_latit)
        else:
            center_point = (0, 0)
        radius = 5
        if my_trip:
            dist = distance.distance(
                center_point, (float(request.user.profile.location_longi or 0.0), float(request.user.profile.location_latit or 0.0))).km
            if dist <= radius:               
                request.user.profile.is_onTrip = True
    return {
        'anon_news': NewsAnnouncements.objects.all(),
    }
    