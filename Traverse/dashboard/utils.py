from django.utils import timezone
from dashboard.models import TravelPlanTrip
from django.core.mail import send_mail
from django.conf import settings
def is_user_online(user):
    now = timezone.now()
    if user.last_login is not None:
        return user.last_login >= now - timezone.timedelta(minutes=5)
    else:
        return False
    
    
def getDestinationPoints(request):
    me_added_trip = []
    for x in TravelPlanTrip.objects.all():
        for i in x.group_users.all():
            if i == request.user:
                me_added_trip.append(
                    [x.longitude[:7], x.latitude[:7], x.place_name, str(x.start_travel_date), str(x.end_travel_date)])
    return me_added_trip

def send_email(subject, message, from_email, to_email):
    return send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[to_email])
    