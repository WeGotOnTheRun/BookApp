from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import Http404, HttpResponseRedirect, reverse
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
        Text = request.GET.get('search')
        books = Book.objects.filter(Q(name__icontains=Text) |Q(summary__icontains=Text))
        authors = Author.objects.filter(name__icontains=Text)
        return render(request, 'library_view/search.html', {'books': books, 'authors': authors})


@login_required
def home(request):
    booklist = []
    followlist = []
    readlist = []
    favcategorylist = []
    favbooklist = []
    recommendedAuthorsList = []
    recommendedBookList = []
    recommendedCategoryList = []
    books = Book.objects.all()
    authors = Author.objects.all()
    category = Category.objects.all()

    if request.user.is_active:
        if request.user is not None and request.user.is_superuser and request.user.is_staff:
            login(request, request.user)
            return HttpResponseRedirect('/admin/')
    try:
        wish = wish_list.objects.filter(user=request.user).values('book')
        for w in wish:
            for getid in w.values():
                for k in books:
                    if k.pk == getid:
                        booklist.append(k)
    except:
        booklist = False

    try:
        wish = Auth_follow.objects.filter(user=request.user).values('author')
        for w in wish:
            for getid in w.values():
                recommendedAuthorsList.append(getid)
                for k in authors:
                    if k.pk == getid:
                        followlist.append(k)
    except:
        followlist = False

    try:
        r = ReadBook.objects.filter(user=request.user).values('book') #book 1
        for w in r:
            for getid in w.values():
                for k in books:
                    if k.pk == getid:
                        readlist.append(k)
    except:
        readlist = False

    try:
        r = FavouriteCategory.objects.filter(user=request.user).values('category') #category 1
        for w in r:
            for getid in w.values():
                recommendedCategoryList.append(getid)
                for k in category:
                    if k.pk == getid:
                        favcategorylist.append(k)
    except:
        favcategorylist = False

    try:
        r = favourite_books.objects.filter(user=request.user).values('book') #category 1
        for w in r:
            for getid in w.values():
                recommendedBookList.append(getid)
                for k in books:
                    if k.pk == getid:
                        favbooklist.append(k)
    except:
        favbooklist = False


    recommend_author = Author.objects.exclude(author_id__in=recommendedAuthorsList)[:3]
    recommend_book = Book.objects.exclude(book_id__in=recommendedBookList)[:3]
    recommend_category = Category.objects.exclude(category_id__in=recommendedCategoryList)[:3]


    return render(request, 'general_view/home.html', {'recommend_book': recommend_book, 'recommend_category': recommend_category, 'recommend_author': recommend_author, 'favbooklist': favbooklist, 'favcategorylist': favcategorylist, 'user': request.user, 'booklist': booklist, 'followlist': followlist,'readlist':readlist})


def show_user(Username):
    try:
        return User.objects.get(username=Username)
    except:
        raise Http404("User Doesn't Exist!")


def profile(request, Username):
    user = show_user(Username)
    return render(request, 'user_view/users.html', {'user': user})
