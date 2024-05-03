from rest_framework import serializers, validators
from .models import User, Profile, Emotions, Task, Community
from django.db import transaction
from django.utils import timezone
from datetime import timedelta


class userSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    image = serializers.URLField()
    def save(self, **kwargs):
        with transaction.atomic():
            user, created = User.objects.get_or_create(email=self.validated_data['email'], username=self.validated_data['username'])
            if not created:
                return user
            Profile.objects.create(user=user, image=self.validated_data['image'])
            return user
    def validate(self, attrs):
        email = attrs.get("email", None)
        if not email:
            raise validators.ValidationError("Email field is required")
        username = attrs.get("username", None)
        if not username:
            raise validators.ValidationError("Username field is required")
        image = attrs.get("image", None)
        if not image:
            raise validators.ValidationError("Image field is required")
        return {
            "email": email,
            "username": username,
            "image": image
        }
    

class emotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotions
        fields = ["user", "emotion", "date"]
        read_only_fields = ["date"]
    


class taskSerializer(serializers.ModelSerializer):
    expired = serializers.SerializerMethodField("is_expired")
    expire = serializers.CharField()
    expire_min = serializers.SerializerMethodField("get_expire_min")

    def create(self, validated_data):
        expire_min = validated_data.pop('expire')
        validated_data['expire'] = self.get_expire(int(expire_min))
        return Task.objects.create(**validated_data)
    

        
    class Meta:
        model = Task
        fields = ['task','user', 'reward', 'done', 'created_at', 'expire', 'user', 'expired', 'category', 'id', "expire_min"]
        read_only_fields = ['expired', 'id']
    
    def get_expire_min(self, instance):
        current_time = timezone.now()
        time_diff = (abs(current_time - instance.expire)).total_seconds()
        return time_diff // 60

    def is_expired(self, task):
        return timezone.now() > task.expire

    def get_expire(self, minutes):
        return timezone.now() + timedelta(minutes=minutes)


class communitySerializer(serializers.ModelSerializer):
    people = serializers.SerializerMethodField("get_user_count")
    class Meta:
        model = Community
        fields = ['users', 'name', 'id', 'people', 'total_points']
        read_only_fields = ['id', 'people']
    
    def get_user_count(self, instance):
        return instance.users.count()

class userProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField("get_username")
    class Meta:
        model = Profile
        fields = ['image', 'github', 'id', 'points', 'username']
    
    def get_username(self, profile):
        return profile.user.username
    
class customCommunitySerializer(serializers.ModelSerializer):
    people = serializers.SerializerMethodField("get_user_count")
    users = serializers.SerializerMethodField("filter_user")
    class Meta:
        model = Community
        fields = ['users', 'name', 'id', 'people', 'total_points']
        read_only_fields = ['id', 'people']
        depth = 2
    
    def get_user_count(self, instance):
        return instance.users.count()

    def filter_user(self, instance):
        users = instance.users.all()
        sorted_users = sorted(users, key=lambda user: user.profile.points, reverse=True)
        serialized_users = []
        for user in sorted_users:
            serialized_users.append({
                "username": user.username,
                "image": user.profile.image,
                "points": user.profile.points,
                "id": user.id
            })
        return serialized_users

        
