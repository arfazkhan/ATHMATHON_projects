from django.urls import path
from . import views

urlpatterns = [
    path("auth/", views.auth),
    path("task/", views.taskView.as_view()),
    path("emotion/", views.emotionApiView.as_view()),
    path("community/", views.communityView.as_view()),
    path("profile/", views.userProfileView.as_view()),
    path("delete-task/", views.deleteTaskView.as_view()),
]
