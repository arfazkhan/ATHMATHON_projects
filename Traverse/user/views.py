from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from dashboard.models import BlogPost, Suggestion
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def home(request):
    return render(request, 'Homepage.html', {
        'blogs': BlogPost.objects.all().order_by('-pub_date')[:4],
    })
@csrf_exempt
def login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        paswd = request.POST['password']
        user = auth.authenticate(username=uname, password=paswd)
        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Login Successfull')
            return redirect('dashboard')  # , { 'result' : uname})
        else:
            messages.warning(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'registration.html')
    
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        uname = request.POST['suname']
        email = request.POST['email']
        native_place = request.POST['nativePlace']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        if pass1 != pass2:
            messages.info(request, 'Password Not Matching')
            return redirect('login')
        if User.objects.filter(username=uname).exists():
            messages.info(request, 'Username Taken')
            return redirect('login')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('login')
        else:
            user = User.objects.create_user(
                username=uname, password=pass1, email=email)
            user.save()
            user.profile.native_place = native_place
            messages.info(request, 'Welcome On Board')
            auth.login(request, user)
            return redirect('dashboard')

    else:
        return render(request, 'Homepage.html')




@login_required(login_url='/login')
def dashboard(request):
    vibes = request.user.profile.vibes.all()
    if vibes.count() > 0:
        suggestions = Suggestion.objects.filter(vibes__in=vibes)
        if suggestions.count() <= 0:
            suggestions = Suggestion.objects.all()
    else:
        suggestions = Suggestion.objects.all()
    context = {
        'suggestions': suggestions,
    }
    return render(request, 'dashboard-enterence.html', context)


def logout(request):
    auth.logout(request)
    return redirect('/')


def ajlogin(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        paswd = request.POST['passwd']
        user = auth.authenticate(username=uname, password=paswd)
        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Login Successfull')
            return JsonResponse(
                {'success': True},
                safe=False
            )
        else:
            return JsonResponse(
                {'success': False},
                safe=False
            )
    else:
        return render(request, 'dashboard-enterence.html')
