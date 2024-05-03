from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field is required")
        email = self.normalize_email(email=email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user





class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    objects = UserManager()
    REQUIRED_FIELDS = ["username", "password"]


class Profile(models.Model):
    image = models.URLField()
    github = models.URLField(null=True)
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user.email


class Emotions(models.Model):
    emotions = {
        "H": "Happy",
        "S": "Sad",
        "A": "Anxious",
        "ST": "Stress",
        "D": "Dipressed"
    }
    emotion = models.CharField(max_length=9, choices=emotions)
    user = models.ForeignKey(User, related_name="emotions", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username

class Task(models.Model):
    categories = {
        "L": "Learning",
        "C": "Cleaning",
        "H": "Fitness",
        "R": "Relation",
        "CA": "Career",

    }
    task = models.CharField(max_length=255)
    reward = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expire = models.DateTimeField()
    user = models.ForeignKey(User, related_name="task", on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=categories, default=categories['L'])


    def __str__(self) -> str:
        return self.task



class Community(models.Model):
    users = models.ManyToManyField(User, related_name="communities")
    name = models.CharField(max_length=100, default="Community")
    total_points = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name