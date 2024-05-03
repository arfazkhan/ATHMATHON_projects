
from django.http import HttpRequest, JsonResponse, HttpResponseNotFound, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from dashboard.utils import getDestinationPoints, send_email
from geopy import distance
from django.contrib.auth.decorators import login_required
from json import dumps
from django.contrib.auth.models import User
from .models import Chat, BlogPost, TravelPlanTrip, FriendRequest, TripRequest, GroupChat, PersonalTravelRequest, Notification
from .forms import ChatForm, BlogPostForm, ProfileForm, TravelPlanForm
from django.utils import timezone   
from user.models import Profile, Review
from django.contrib import messages
from user.models import Vibes
import json
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def vibe_selection(request):
    if request.method == "POST":
        vibes = Vibes.objects.filter(name__in=json.loads(request.body.decode("utf-8")))
        request.user.profile.vibes.set(vibes)
        return JsonResponse({"success": True})

    return render(
        request,
        "vibe_selection.html",
        {
            "vibes": Vibes.objects.all(),
            
        },
    )
@login_required(login_url='/')
def home(request):
    return render(request, 'Homepage.html')


@login_required(login_url='/')
def companion(request: HttpRequest) -> HttpResponse:
    destination_points = getDestinationPoints(request)
    if (user_profile := Profile.objects.filter(user=request.user).first()) is not None and user_profile.location_latit != "" and user_profile.location_longi != "":
        center_point = (user_profile.location_longi, user_profile.location_latit)
    else:
        center_point = (0, 0)
    radius = 2.6 
    points = Profile.objects.exclude(user=request.user).values('id', 'user_id', 'native_place', 'is_online', 'first_name', 'last_name', 'email', 'number', 'profile_pic', 'is_onTrip', 'bio', 'personal_favorite_trip_blog', 'location_longi', 'location_latit')
    points_within_radius = []
    for profile in points:
        if profile['location_latit'] is not None and profile['location_longi'] is not None:
            profile['username'] = User.objects.get(id=profile['user_id']).username
            dist = distance.distance(
                center_point, (float(profile['location_longi']), float(profile['location_latit']))).km
            if dist <= radius:
                print(dist, profile)
                points_within_radius.append(profile)
    
    return render(request, 'companion.html', {'points': dumps(points_within_radius), 'destination_points': dumps(destination_points)})


@login_required(login_url='/')
def save_location(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        latitude: str = request.POST.get('latitude')
        longitude: str = request.POST.get('longitude')
        user: User = request.user
        user_prof: Profile = Profile.objects.get(user=user)
        user_prof.location_longi = longitude
        user_prof.location_latit = latitude
        user_prof.save()
        return JsonResponse({'status': 'success'})


@login_required(login_url='/')
def friends(request):
    sended_requests = FriendRequest.objects.filter(from_user=request.user)
    sended_users = [x.to_user for x in sended_requests]    
    try:
        search_query = request.GET['search']
        profiles = Profile.objects.filter(
            Q(user__username__icontains=search_query))
    except KeyError:
        profiles = Profile.objects.all().exclude(user=request.user)
    profiles = sorted(profiles, key=lambda profile: profile.vibes.filter(pk__in=request.user.profile.vibes.all()).count(), reverse=True)    
    return render(request, 'friends.html', {
        'profiles': profiles,
        'sended_users': sended_users
    })


def add_friend(request, id):
    if request.user != None:
        if not FriendRequest.objects.filter(from_user=request.user, to_user=User.objects.get(id=id)).exists():
            FriendRequest.objects.create(
                from_user=request.user, to_user=User.objects.get(id=id))
    return redirect('friends')


@login_required(login_url='/')
def remove_friend(request, id):
    request.user.profile.friends.remove(User.objects.get(id=id))
    User.objects.get(id=id).profile.friends.remove(request.user)
    return redirect('friends')


@login_required(login_url='/')
def remove_request(request, id):
    ob = FriendRequest.objects.get(from_user=request.user,
                                   to_user=User.objects.get(id=id))
    ob.delete()
    return redirect('friends')


@login_required(login_url="/")
def notifications(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        try:
            if "add_friend" in request.POST:
                user_id = int(request.POST["user_id"])
                user = User.objects.get(id=user_id)
                request.user.profile.friends.add(user)
                user.profile.friends.add(request.user)
                FriendRequest.objects.get(to_user=request.user, from_user=user).delete()
                messages.success(request, f"{user.username} is Your Friend!")
                Notification.objects.create(
                    to_user=user, from_user=request.user, message="You are friends with " + user.username
                )
            elif "delete" in request.POST:
                notif = int(request.POST['notif'])
                Notification.objects.get(id=notif).delete()
            elif "add_trip" in request.POST:
                req = int(request.POST['req'])
                user_id = int(request.POST["user"])
                trip_id = int(request.POST["add_trip"])
                TravelPlanTrip.objects.get(id=trip_id).group_users.add(User.objects.get(id=user_id))
                TripRequest.objects.get(id=req).delete()
        except Exception as e:
            print(e)
            messages.error(request, "An error occurred. Please try again.")

    return render(
        request,
        "notifications.html",
        {
            "friend_requests": FriendRequest.objects.filter(to_user=request.user),
            'personel_trip_requests': TripRequest.objects.filter(to_trip__user=request.user),
            "notifications": Notification.objects.filter(to_user=request.user),
        },
    )


def del_not(request, id):
    Notification.objects.get(id=id).delete()
    return redirect('notifications')



@ login_required(login_url='/')
def profile(request: HttpRequest) -> HttpResponse:
    profile: Profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect('profile')
        else:
            print("not valid")
            print(form.errors)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {
        'latitude': profile.location_latit,
        'longitude': profile.location_longi,
        'form': form,
        'profile': profile,
        'tags': request.user.profile.vibes.all(),
    })


@ login_required(login_url='/')
def blog(request):
    blogs = BlogPost.objects.all()
    form = BlogPostForm()
    if request.method == 'POST':
        print(request.POST)
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            print('is Valid')
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = timezone.now()
            post.save()
            return redirect('blog')
        else:
            return HttpResponse("Form Is Not Valid", status=401)
    return render(request, "pblog.html", context={'form': form, 'blogs': blogs})


def blog_detail(request, id):
    blog = BlogPost.objects.get(id=id)
    form = BlogPostForm(instance=blog)
    if request.method == 'POST':
        if request.POST['type'] == 'edit':
            form = BlogPostForm(request.POST, request.FILES, instance=blog)
            if form.is_valid():
                form.save()
        else:
            blog.delete()
            return redirect('blog')
    return render(request, "blog-detail.html", {
        'blog': blog,
        'form': form
    })


def like_post(request, id, status):
    post = BlogPost.objects.select_related(
        'author').prefetch_related('likes').get(id=id)
    if status == 0:
        user = request.user
        likes = post.likes.all()
        if user in likes:
            post.likes.remove(user)
            status = False
        else:
            post.likes.add(user)
            status = True
        post.save()
        likes_count = post.likes.count()
        likes_names = [like.username for like in likes]
        response_data = {
            'author': post.author.username,
            'likes_count': likes_count,
            'likes_names': likes_names,
            'status': status
        }
        return JsonResponse(response_data)
    liked = False
    if request.user in post.likes.all():
        liked = True
    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })




@csrf_exempt
def trip_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if data['isOnTrip']:
            request.user.profile.is_onTrip = True
            request.user.profile.save()
        else:
            request.user.profile.is_onTrip = False
            request.user.profile.save()
            
    return JsonResponse({"status": True})



@login_required(login_url='/')
def plantrip_group_chat(request, id):
    messages = GroupChat.objects.filter(receiver=id)
    return render(request, 'plantrip_group_chat.html', {
        'trip': TravelPlanTrip.objects.get(id=id),
        'messages': messages
    })


@ login_required(login_url='/')
def chat(request):
    old_friends = []
    for x in Chat.objects.all():
        if x.sender == request.user:
            old_friends.append(x.receiver)
    return render(request, 'chat.html', {
        'messages': Chat.objects.all(),
        'old_friends': old_friends
    })


@ login_required(login_url='/')
def person_chat(request):
    form = ChatForm()
    receiver = get_object_or_404(User, username=request.GET.get('username'))
    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.sender = request.user
            chat.receiver = receiver
            chat.save()
        else:
            print(form.errors)
    context = {
        'form': form,
        'receiver': receiver,
        'messages': Chat.objects.filter(sender=request.user, receiver=receiver) | Chat.objects.filter(sender=receiver, receiver=request.user)
    }
    if request.user != User.objects.get(username=request.GET.get('username')):
        return render(request, 'person_chat.html', context)
    else:
        return HttpResponseNotFound()


def send_travel_request(request, id, user_id):
    if not PersonalTravelRequest.objects.filter(from_user=request.user, to_user=User.objects.get(username=id), trip=TravelPlanTrip.objects.get(id=id)).exists():
        PersonalTravelRequest.objects.create(to_user=User.objects.get(
            username=user_id), from_user=request.user, trip=TravelPlanTrip.objects.get(id=id))
    return redirect('dashboard')




def send_bulk_email(request, id):
    travel = TravelPlanTrip.objects.get(id=id)
    if travel:
        users = travel.group_users.all()
        emails = [user.profile.email for user in users]
        usernames : str = ", ".join([user.username for user in users]) 
        for email in emails:
            send_email(
                subject="Trip Reminder",
                message=f"""
Trip to {travel.place_name} | {travel.mode_of_travel}
--------------------------------------------------
Trip Start Date is {travel.start_travel_date} To {travel.end_travel_date}.

Total Users: {usernames}
----------------+---------------+----------------+
                """,
                from_email="eesaard@gmail.com",
                to_email=email
            )
    return redirect('plantrip-detail', travel.id)


def review(request):
    profiles = Profile.objects.exclude(
        user=request.user).prefetch_related(
            'reviews', 'reviews__user')
    if request.method == "POST":
        message = request.POST.get('review')
        value = request.POST.get('value')
        author = request.user
        user_id = request.POST.get('user')
        if user_id is not None:
            try:
                user = User.objects.get(id=user_id)
                inst = Review.objects.create(
                    review=message, value=value, user=author)
                print(inst, user)
                user.profile.reviews.add(inst)
                
            except User.DoesNotExist:
                pass
    return render(request, 'review.html', {
        'profiles': profiles
    })




@login_required(login_url='/')
def plantrip(request):
    form = TravelPlanForm()
    datas = []
    if request.method == 'POST':
        print(request.POST)
        form = TravelPlanForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            instance.group_users.add(request.user)
        else:
            print(form.errors)
    for x in TravelPlanTrip.objects.all():
        if x.mode_of_travel == 'solo':
            if x.user in request.user.profile.friends.all() or x.user == request.user:
                if x.group_users.all().count() < 2 or request.user in x.group_users.all():
                    datas.append(x)
        else:
            datas.append(x)
            
    
    return render(request, 'plantrip.html', {
        'plans': datas,
    })


@login_required(login_url='/')
def plantrip_detail(request, id):
    ob = TravelPlanTrip.objects.get(id=id)
    return render(request, 'plan_trip_detail.html', {
        'trip': ob,
        'requests': TripRequest.objects.filter(to_trip=ob),
        'is_requested': TripRequest.objects.filter(to_trip=ob, from_user=request.user).exists(),
        'personel_trip_is_requested': PersonalTravelRequest.objects.filter(trip=ob, from_user=request.user),
    })


@login_required(login_url='/')
def plan_trip_delete(request, id):
    if (TravelPlanTrip.objects.get(id=id).user == request.user):
        TravelPlanTrip.objects.get(id=id).delete()
    return redirect('plantrip')


@login_required(login_url='/')
def plantrip_add_user(request: HttpRequest, id: int) -> HttpResponse:
    trip: TravelPlanTrip = TravelPlanTrip.objects.get(id=id)
    if not TripRequest.objects.filter(from_user=request.user, to_trip=trip).exists() and trip.mode_of_travel == 'team':
        TripRequest.objects.create(
            from_user=request.user, to_trip=trip)
    if not TripRequest.objects.filter(from_user=request.user, to_trip=trip).exists() and trip.mode_of_travel == 'solo':
        if trip.group_users.all().count() < 2:
            TripRequest.objects.create(
                from_user=request.user, to_trip=trip)
        else:
            messages.error(
                request, 'You can not add more than 4 people to a trip')
    return redirect('plantrip-detail', id)


@login_required(login_url='/')
def plantrip_add_user_accept(request, id, trip_id):
    x = TripRequest.objects.get(id=id)
    print(x.to_trip.group_users.all())
    x.to_trip.group_users.add(x.from_user)
    x.delete()
    Notification.objects.create(
        to_user=x.from_user,
        from_user=x.to_trip.user,
        message=f'You Join Request To {TravelPlanTrip.objects.get(id=trip_id).place_name} Trip Has Accepted'
    )
    return redirect('plantrip-detail', trip_id)

@csrf_exempt
@login_required(login_url='/')
def plantrip_add_user_declined(request, id, trip_id):
    TripRequest.objects.get(id=id).delete()
    return redirect('plantrip-detail', trip_id)


@login_required(login_url='/')
def plantrip_leave_user(request, id):
    TravelPlanTrip.objects.get(id=id).group_users.remove(request.user)
    return redirect('plantrip-detail', id)



def travel_plan_list(request):
    travel_plans = TravelPlanTrip.objects.all()
    return render(request, 'Homepage.html', {'travel_plans': travel_plans})
    