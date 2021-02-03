from django.shortcuts import render, redirect
from .forms import AddBizForm,AnnouncementForm,UserRegistrationForm 
from .models import User, Business,Announcement, Blog,Essential,Meeting
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from .forms import UserRegistrationForm, UserLoginForm, AddBizForm
from .models import User, Hood, Business, Profile

def register(request):
    if request.method == 'POST' and register_user(request):
        return redirect('/login')    
    registerform = UserRegistrationForm()        
    return render(request, "registration_form.html", {'register_form': registerform})

def logIn(request):
    if request.method == 'POST' and request.POST.get('username') and request.POST.get('password'):
        if validate_and_login_user(request):
            return redirect('/profile')
    loginform = UserLoginForm()
    return render(request, 'login.html', {'login_form': loginform})

@login_required(login_url='/login')
def home(request):
    user = request.user
    if not Profile.objects.filter(user=user).exists():
        return redirect('/profile')
    user_hood = user.profile.reach
    businesses_in_hood = Business.objects.filter(hood = user_hood) 
    news_in_hood = Announcement.objects.filter(hood = user_hood)
    meetings_in_hood = Meeting.objects.filter(hood = user_hood)
    essentials_in_hood = Essential.objects.filter(hood =user_hood)
    
    return render(request, "index.html", {'businesses': businesses_in_hood, 'announcements': news_in_hood,'meetings':meetings_in_hood,'essentials':essentials_in_hood})
    


@login_required(login_url='/login')
def profile(request):
    if request.method == 'POST' and change_profile_picture(request):
        return redirect('/profile') # To access the profile image of the user -> user.picture.url
    elif request.method == 'POST' and change_profile(request):
        return redirect('/profile')
        
    user = request.user
    hoods = Hood.get_all_hoods()
    return render(request, 'profile.html', {'user': user, 'hoods': hoods})


#Announcement page
def announcement(request):
    news = Announcement.objects.all()     
    return render(request, "announcement.html",{"news":news})

def create_announcement(request):
    current_user = request.user
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.user = current_user
            announcement.save()
        return redirect('index')    
    else:
        form = AddBizForm
    return render(request, 'new-announcement.html', {'form':form})   

#Blog page
def blog(request):
    blogs = Blog.objects.all()
    return render(request, "blog.html", {'blogs': blogs})

#Business page
def business(request):
    hood = request.user.profile.reach
    biznas = Business.objects.filter(hood = hood.id)
    
    return render(request, "business.html",{"biznas":biznas})

def selected_business(request, id):
    biz = Business.objects.get(id = id)
    to_display_biz = []
    to_display_biz.append(biz)

    return render(request, 'business.html',{"businesses": to_display_biz})


def selected_meeting(request, id):
    meeting = Meeting.objects.get(id = id)
    to_display_meeting = []
    to_display_meeting.append(meeting)

    return render(request, 'meeting.html',{"meetings": to_display_meeting})


def selected_essential(request, id):
    essential = Essential.objects.get(id = id)
    to_display_essential = []
    to_display_essential.append(essential)

    return render(request, 'essential.html',{"essentials": to_display_essential})


def create_business(request):
    current_user = request.user
    if request.method == 'POST' and current_user.is_admin == True:
        form = AddBizForm(request.POST, request.FILES)
        if form.is_valid():
            biz = form.save(commit=False)
            biz.user = current_user
            biz.hood = current_user.profile.reach
            biz.save()
        return redirect('/business')    
    else:
        form = AddBizForm
    return render(request, 'new-biz.html', {'form':form})        

#Meeting page
def meeting(request):
    meetings = Meeting.objects.filter(hood = request.user.profile.reach.id)
    return render(request, "meeting.html", {'meetings':meetings})

 
#Essentials page
def essential(request):
    essentials = Essential.objects.filter(hood = request.user.profile.reach.id)
    return render(request, "essential.html", {'essentials':essentials})



def register_user(request):
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
        form.save()
        return True
    else:
        return False


def check_if_user_exist(username, password):
    if username == None or password == None:
        return False
    return User.objects.filter(username = username).exists()

def authenticate_user(request, username, password):
    return authenticate(request, username= username, password = password)
  
def validate_and_login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user_exists = check_if_user_exist(username, password)
    if user_exists:
        user = authenticate_user(request, username, password)
    else:
        return False
    if user:
        login(request, user)
        return True  
    return render(request, "index.html")



def change_profile_picture(request):
    user = request.user
    profile_image = request.FILES.get('profile')
    if profile_image:
        user.picture = profile_image
        user.save()
        return True
    else:
        return False


def change_profile(request):
    user = request.user
    name = request.POST.get('name')
    name_field = 'name'
    location = request.POST.get('location')
    location_field = 'location'
    reach = request.POST.get('reach')
    reach_field = 'reach'
    reach = request.POST.get('reach')
    reach_field = 'reach'

    if name:
        change_field(user, name_field, name)
    if location:
        change_field(user, location_field,location)
    if reach:
        reach = Hood.objects.get(id = int(reach))
        change_field(user, reach_field,reach)
    
    if not name and not location and not reach:
        return False
    else: return True

def change_field(user, field_name, field_value):
    if check_if_user_has_profile(user):
        setattr(user.profile, field_name, field_value)
        user.profile.save()
    else:
        create_profile_for_user(user) 
        setattr(user.profile, field_name, field_value)
    user.save()

    
def check_if_user_has_profile(user):
    return Profile.objects.filter(user=user.id).exists()
    
def create_profile_for_user(user):
    hood = Hood.objects.get(id = 1)
    user_profile = Profile(name = '', location='', user= user, reach=hood)
    user.profile = user_profile
    user_profile.save()
    user.save()
    return True

def search_results(request):

    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        searched_businesses = Business.search_by_name(search_term)
        message = f"{search_term}"

        return render(request, 'business.html',{"message":message,"businesses": searched_businesses})

    else:
        message = "You haven't searched for any term"
        return render(request, 'business.html',{"message":message})
