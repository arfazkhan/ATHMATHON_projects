from django.contrib import admin
from . import models

admin.site.register([models.User, models.Profile, models.Task, models.Emotions, models.Community])
