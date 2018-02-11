from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import Http404
from django.contrib.auth.models import User
from helper import db_helper

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
            user = authenticate(username=user.username, password=password)
            login(request, user)
            print('done')
            return redirect('home')
    else:
        form = SignUp()
    return render(request, 'user_view/signup.html', {'form': form})


@login_required
def home(request):
    db_helper.ini_countries()
    return render(request, 'general_view/home.html')

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
