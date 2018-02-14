from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import Http404,HttpResponseRedirect, reverse
from helper import db_helper
<<<<<<< HEAD
from django.http import HttpResponse
from django.db.models import Q
from library.models  import Book,Author
from django.views.decorators.csrf import csrf_exempt
=======
from django1 import settings
from django.contrib.auth.views import login as auth_login
from django.contrib.auth import authenticate, login
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
>>>>>>> 63c793563747b27fd997ba14af1360a3edb9e16d

# hash this line after using it.
# db_helper.ini_countries()


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
            # user = authenticate(username=user.username, password=password)
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
    db_helper.ini_countries()
    if request.user.is_active:
        if request.user is not None and request.user.is_superuser and request.user.is_staff:
            login(request, request.user)
            return HttpResponseRedirect('/admin/')
    return render(request, 'general_view/home.html')
<<<<<<< HEAD

#
# @login_required
# def profile(request):
#     # user = show_user(username)
#     return render(request, 'user_view/profile.html')
#
#
# def show_user(username):
#     try:
#         return User.objects.get(Username=username)
#     except:
#         raise Http404("User Doesn't Exist!")
#
=======
>>>>>>> 63c793563747b27fd997ba14af1360a3edb9e16d
