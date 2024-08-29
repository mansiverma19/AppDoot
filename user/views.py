from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from rest_framework.response import Response
from .serializers import UserSerializer
from android.serializers import AppSerializer, UserAppsSerializer
from android.models import *
from .models import Profile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as django_login,logout as django_logout
import requests
import os

# Home view for authenticated users
def home(request):
    print(request.user.is_authenticated) 
    return render(request, 'user/home.html')

def signup_view(request):
    return render(request, 'user/signup.html')

def login_view(request):
    return render(request, 'user/login.html')

# Registration view
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("***************************",username,email,password)
        data = {     
                    "username": username,
                    "password": password,
                    "email": email
        }
        response = requests.post(settings.BASE_URL+'api/v1/users/', data=data)
        if response.status_code == 201:
            print("----------success---------------")
            return redirect('login')
        else:
            return JsonResponse(response.json(), status=response.status_code)
    return render(request, 'user/signup.html')

# # Login view
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(settings.BASE_URL+'api/v1/users/login/', json=data)
        
        if response.status_code == 200:
            user = authenticate(username=username, password=password)
            response_data = response.json()
            access_token = response_data.get('access')
            # Optionally, you can set the token or session ID in the user's session or local storage
            request.session['access_token'] = access_token
            django_login(request, user)
            # Redirect or render based on user data
            user_data = response_data.get('user_data')
            if user_data and user_data.get('is_staff'):
                test(request=request)
                return render(request, 'admin/admin.html')
            else:
                test(request=request)
                return redirect('home')
        else:
            return JsonResponse(response.json(), status=response.status_code)
    return render(request, 'user/login.html')

def logout_view(request):
    # Send POST request to API to logout the user
    response = requests.post(settings.BASE_URL+'api/v1/users/logout/')
    if response.status_code == 200:
        django_logout(request)  # Log out the user from the Django session
    return redirect('home')

def test(request):
    print('-------------------------------',request)
    if request.user.is_authenticated:
        user = request.user
        print(user)

def user_profile(request):
    user = request.user
    completed_tasks = UserApps.objects.filter(user=user, is_completed=True)
    pending_tasks = UserApps.objects.filter(user=user, is_completed=False)
    incompleted_apps = App.objects.exclude(userapps__user=user)
    count={
        'completed':len(completed_tasks),
        'pending':len(pending_tasks),
        'incompleted':len(incompleted_apps)
    }
    return render(request, 'user/user_profile.html', {'user': request.user,'completed_tasks':completed_tasks,'count':count})

# Shows all completed incompleted and pending tasks
def user_tasks_view(request):
    user = request.user
    completed_tasks = UserApps.objects.filter(user=user, is_completed=True)
    pending_tasks = UserApps.objects.filter(user=user, is_completed=False)
    uncompleted_apps = App.objects.exclude(userapps__user=user)
    for i in uncompleted_apps:
        print(i.name)
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'uncompleted_apps': uncompleted_apps,
    }

    print(context)
    return render(request, 'user/user_tasks.html', context)

# When user clicks on incompleted tasks - install_complete
@login_required
def app_page(request):
    if request.method == 'POST':
        app_name = request.POST.get('app_name')
        app = get_object_or_404(App, name=app_name)
        return render(request, 'admin/app_page.html', {'app': app})  
    return redirect('task_page')

# Handles the screenshot upload 
@login_required
def upload_screenshot(request, app_id):
    app = get_object_or_404(App, id=app_id)
    if request.method == 'POST':
        print(request.FILES)
        if 'screenshot-field' in request.FILES:
            screenshot = request.FILES['screenshot-field']
            if screenshot:
                # code to save uploaded app logo in static/app_logos folder
                ss_directory = os.path.join('AppDoot', 'static', 'screenshots')
                if not os.path.exists(ss_directory):
                    os.makedirs(ss_directory)  

                # Save the file to the specified path
                fs = FileSystemStorage(location=ss_directory)
                filename = fs.save(screenshot.name, screenshot)

            user_app = UserApps.objects.create(
                user=request.user,
                app=app,
                screenshot=screenshot,
                points_earned=app.points,
                is_completed=False
            )
            user_app.save()
            return redirect('user_tasks')  # Redirect to the user tasks page
        else:
            messages.error(request, "Please upload a screenshot.")
            return redirect('install_complete', app_id=app_id)
    return redirect('install_complete', app_id=app_id)

# Calls api from android app to handle upload of new app by admin
def Add_app(request):
    return render(request, 'admin/add_apps.html')

@login_required
def Add_app_submit(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        url = request.POST.get('url')
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')
        points = int(request.POST.get('points'))
        uploaded_file = request.FILES.get('logo')
        
        if uploaded_file:
            # code to save uploaded app logo in static/app_logos folder
            logo_directory = os.path.join('AppDoot', 'static', 'app_logos')
            if not os.path.exists(logo_directory):
                os.makedirs(logo_directory)  

            # Save the file to the specified path
            fs = FileSystemStorage(location=logo_directory)
            filename = fs.save(uploaded_file.name, uploaded_file)
            uploaded_file_path = fs.path(filename)
            print(uploaded_file_path)
        
            # Save app details to the database
            app = App(
                name=name,
                url=url,
                category=category,
                sub_category=sub_category,
                points=points,
                logo=uploaded_file  # Save only the filename or path if needed
            )
            app.save()

            return redirect('ListApps')

        return redirect('add_app')

# lists all apps added by admin 
def List_Apps(request):
    all_apps = App.objects.all()
    return render(request, 'admin/list_apps.html', {'all_apps': all_apps}) 

@login_required
def admin_pending_tasks(request):
    if not request.user.is_staff:
        return redirect('home')  # Redirect if the user is not an admin

    tasks = UserApps.objects.filter(is_completed=False)
    return render(request, 'admin/admin_pending_tasks.html', {'tasks': tasks})

@login_required
def accept_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(UserApps, id=task_id)
        task.is_completed = True
        task.save()

         # Get the user's profile and update the total points
        user_profile = Profile.objects.get(user=task.user)
        user_profile.total_points += task.points_earned
        user_profile.save()
        return redirect('admin_pending_tasks')  # Redirect to the pending tasks page

    return redirect('admin_pending_tasks')  