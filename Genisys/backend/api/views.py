from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.decorators import api_view
from .google_auth import create_token
from . import serializer as serial, models
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import transaction


@api_view(['POST'])
def auth(request):
    try:
        serializer = serial.userSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        user = serializer.save()
        simple_jwt_tokens = create_token(user=user)

        return Response(simple_jwt_tokens)
    
    except Exception as e:
        print(e)
        return Response({"Error": "server error"}, status=500)


class emotionApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            data = {**request.data, "user": request.user.id}
            serializer = serial.emotionSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            serializer.save()
            return Response(serializer.data, status=201)

        except Exception as e:
            print(e)
            return Response({"error": "Server error"}, status=500)
    
    def get(self, request, *args, **kwargs):
        try:
            emotions = request.user.emotions.all()
            serializer = serial.emotionSerializer(emotions, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({"error": "Server error"}, status=500)
    
class taskView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            data = {**request.data, "user": request.user.id}
            serializer = serial.taskSerializer(data=data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            result = serializer.save()
            return Response(serializer.data, status=201)

        except Exception as e:
            print(e)
            return Response({"error": "Server error"}, status=500)
        
    def get(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            category = request.query_params.get("category", None)
            if category:
                done_taskes = models.User.objects.prefetch_related("task").get(id=user_id).task.filter(category=category, done=True)
                not_done_taskes = models.User.objects.prefetch_related("task").get(id=user_id).task.filter(category=category, done=False)
            else:
                done_taskes = models.User.objects.prefetch_related("task").get(id=user_id).task.filter(done=True)
                not_done_taskes = models.User.objects.prefetch_related("task").get(id=user_id).task.filter(done=False)
            done_serializer = serial.taskSerializer(done_taskes, many=True)
            not_done_serializer = serial.taskSerializer(not_done_taskes, many=True)
            return Response({"done": done_serializer.data, "not_done": not_done_serializer.data})
        except Exception as e:
            print(e)
            return Response({"error": "Server error"}, status=500)
    
    def patch(self, request, *args, **kwargs):
        try:
            task_id = request.data['id']
            with transaction.atomic():
                user = request.user
                task = models.Task.objects.get(id=task_id)
                task.done = True
                task.save()
                user_profile = request.user.profile
                user_profile.points += 50
                user_profile.save()
                communities = user.communities.all()
                for community in communities:
                    print("updating total points")
                    community.total_points += 50
                    community.save()
                return Response({"message": "success"})
        except models.Task.DoesNotExist as e:
            print(e)
            return Response({"error": "Task with id not found"}, status=404)
        except Exception as e:
            print(e)
            return Response({"error": "Server error"}, status=500)


class communityView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            data = {**request.data, "users": [request.user.id]}
            serializer = serial.communitySerializer(data=data)
            if not serializer.is_valid():
                return Response({"error": "Bad request"}, status=400)
            instance = serializer.save()
            instance.total_points = request.user.profile.points
            instance.save()
            return Response(serializer.data)

        except Exception as e:
            print(e)
            return Response({"error": "Server error"}, status=500)
    
    
    def get(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            community_name = request.query_params.get("name")
            mine = request.query_params.get("my")
            community_id = request.query_params.get("id")
            if community_name:
                community = models.Community.objects.filter(name__contains=community_name)
            elif mine:
                community = models.Community.objects.filter(users__id=user_id).order_by("total_points")
            elif community_id:
                community = models.Community.objects.get(id=community_id)
                serializer = serial.customCommunitySerializer(community)
                return Response(serializer.data)
            else:
                community = models.Community.objects.all()

            serializer = serial.communitySerializer(community, many=True)
            return Response(serializer.data)
        
        except Exception as e:
            print(e)
            return Response({"error": "Server error"}, status=500)
    
    def patch(self, request, *args, **kwargs):
        try:
            user = request.user
            community_id = request.query_params.get("id")
            if not community_id:
                return Response({"error": "query param community not found"}, status=400)
            community = models.Community.objects.get(id=community_id)
            community.users.add(user)
            community.total_points += user.profile.points
            community.save()

            return Response({"message": "success"})
        
        except Exception as e:
            print(e)
            return Response({"error": "Server error"}, status=500)


class userProfileView(APIView):


    def get(self, request, *args, **kwargs):
        try:
            user_id = request.query_params.get('id')
            is_mine = request.query_params.get("my")

            if is_mine:
                user_profile = models.User.objects.prefetch_related('profile').get(id=request.user.id).profile
            else:
                user_profile = models.User.objects.prefetch_related('profile').get(id=user_id).profile

            serializer = serial.userProfileSerializer(user_profile)
            return Response(serializer.data)
        
        except Exception as e:
            print(e)
            return Response({"error": "Server error"}, status=500)


    def patch(self, request, *args, **kwargs):
        try:
            user = request.user
            data = request.data
            instance = user.profile
            serializer = serial.userProfileSerializer(instance=instance, data=data, partial=True)
            if not serializer.is_valid():
                return Response({"error": "Bad request"}, status=400)
            serializer.save()
            return Response({"message": "success"})
        
        except Exception as e:
            print(e)
            return Response({"error": "Server error"}, status=500)


class deleteTaskView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            task_id = request.data['id']
            task = models.Task.objects.get(id=task_id)
            task.delete()
            return Response({"message": "success"})
        
        except Exception as e:
            print(e)
            return Response({"error": "Server error"}, status=500)