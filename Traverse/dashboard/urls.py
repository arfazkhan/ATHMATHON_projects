from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/vibes/', views.vibe_selection, name='vibe-selection'),
    path('dashboard/companion', views.companion, name='companion'),
    path('dashboard/companion/location',
         views.save_location, name='companion-location'),
    
     path('dashboard/friends', views.friends, name='friends'),
    path('dashboard/profile', views.profile, name='profile'),
    path('dashboard/friends/add_friend/<int:id>/add',
         views.add_friend, name='add_friend'),
    path('dashboard/friends/remove_friend/<int:id>/remove',
         views.remove_friend, name='remove_friend'),
    path('dashboard/friends/remove_request/<int:id>/remove',
         views.remove_request, name='remove_request'),
    path('dashboard/friends/notifications/',
         views.notifications, name='notifications'),

    path('dashboard/noti/<int:id>/delete',
         views.del_not, name='del-not'),
    
        path('dashboard/blog', views.blog, name='blog'),
    path('dashboard/blog/detail/<int:id>/',
         views.blog_detail, name='blog-detail'),
    path('dashboard/blog/detail/<int:id>/like/<int:status>',
         views.like_post, name='like_post'),
    
    
    
        path('dashboard/plantrip', views.plantrip, name='plantrip'),
    path('dashboard/plantrip/<int:id>/trip',
         views.plantrip_detail, name='plantrip-detail'),
    path('dashboard/plantrip/<int:id>/trip/delete',
         views.plan_trip_delete, name='plantrip-delete'),
    path('dashboard/plantrip/<int:id>/trip/add_user',
         views.plantrip_add_user, name='plantrip-add-user'),
    path('dashboard/plantrip/<int:id>/trip/leave_user',
         views.plantrip_leave_user, name='plantrip-leave-user'),

    path('dashboard/plantrip/<int:id>/<int:trip_id>/trip/add_user_accept',
         views.plantrip_add_user_accept, name='plantrip-add-user-accept'),
    path('dashboard/plantrip/<int:id>/<int:trip_id>/trip/add_user_decline',
         views.plantrip_add_user_declined, name='plantrip-add-user-decline'),         
     path('dashboard/travel-plans/', views.travel_plan_list, name='travel-plan-list'),


    path('dashboard/plantrip/<int:id>/trip/groupchat',
         views.plantrip_group_chat, name='plantrip_group_chat'),
    path('dashboard/chat/', views.chat, name='chat'),
    path('dashboard/chat/person-chat', views.person_chat, name='person-chat'),
         path('dashboard/trip_status/', views.trip_status, name='trip_status'),

    path('dashboard/plantrip/detail/<int:id>/request/<slug:user_id>',
         views.send_travel_request, name='send_travel_request'),
    
    
    path('dashboard/plantrip/detail/<int:id>/send_emails', views.send_bulk_email, name="send_bulk_email"),
    
    path('dashboard/review/', views.review, name="review")
    
    ]
