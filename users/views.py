from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import Http404, HttpResponseRedirect, reverse
from helper import db_helper
from django1 import settings
from django.contrib.auth.views import login as auth_login
from django.contrib.auth import authenticate, login
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models import Q
from library.models import *
from django.views.decorators.csrf import csrf_exempt


def sign_up(request):
    if request.method == 'POST':
        form = SignUp(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.picture = form.cleaned_data.get('picture')
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=password)
            login(request, user)
            print('done')
            return redirect('library:index')
    else:
        form = SignUp()
    return render(request, 'general_view/signup.html', {'form': form})


@login_required
def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user.user.is_active:
            if request.user is not None and request.user.is_superuser and request.user.is_staff:
                login(request, request.user)
                return HttpResponseRedirect('/admin/')
            else:
                login(request, user)
                return redirect('/')
        return auth_login(request, {'template_name': 'login.html'})

@csrf_exempt
def search(request):
        Text=request.GET.get('search')
        books = Book.objects.filter(Q(name__icontains=Text) |Q(summary__icontains=Text))
        authors=Author.objects.filter(name__icontains=Text)
        return render(request,'library_view/search.html',{'books':books,'authors':authors})


@login_required
def home(request):
    if request.user.is_active:
        if request.user is not None and request.user.is_superuser and request.user.is_staff:
            login(request, request.user)
            return HttpResponseRedirect('/admin/')
    try:
        wish = wish_list.objects.filter(user=request.user).values()
        book = Book.objects.all()
    except:
        wish = False
        book = False
    return render(request, 'general_view/home.html', {'wish': wish, 'book':book})


def show_user(Username):
    try:
        return User.objects.get(username=Username)
    except:
        raise Http404("User Doesn't Exist!")


def profile(request, Username):
    user = show_user(Username)
    #if user = current user
        #redirect('profile')
    #else
    return render(request, 'user_view/users.html', {'user': user})
