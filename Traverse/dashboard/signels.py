from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TravelPlanTrip


@receiver(post_save, sender=TravelPlanTrip)
def create_travel_group(sender, instance, created, **kwargs):
    if created:
        print("From Signel: Item Created")
