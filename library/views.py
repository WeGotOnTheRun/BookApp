from .models import *
from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.utils import timezone
from users.models import *
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from helper import db_helper


def get_picture(request):
    user = request.user
    return user


def index(request):
    # db_helper.ini_countries()
    books = Book.objects.all().order_by('-book_id')[:3]
    authors = Author.objects.all()[:3]
    categories = Category.objects.all()[:3]
    book_no = Book.objects.count()
    author_no = Author.objects.count()
    category_no = Category.objects.count()
    active_user = 0
    users = User.objects.count()
    try:
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
        user_id_list = []
        for session in active_sessions:
            data = session.get_decoded()
            user_id_list.append(data.get('_auth_user_id', None))
            active_user = User.objects.filter(id__in=user_id_list).count()
    except:
        active_user = 0


    return render(request, 'library_view/index.html',{'users':users,'follow': follow, 'books': books, 'authors': authors, 'categories': categories, 'book_no': book_no, 'category_no':category_no,'author_no':author_no, 'active_user':active_user})


class BookListView(ListView):
    model = Book
    template_name = 'library_view/book_list.html'


class BookDetailView(DetailView):
    model = Book
    template_name = 'library_view/book_detail.html'

    def get_context_data(self,* args,**kwargs):
        readlist = []
        ctx =super(BookDetailView, self).get_context_data(*args, **kwargs)
        books = self.get_object().pk
        ctx['categoryBooks'] = Book.objects.get(pk=books).Category.all()
        ctx["book"] = self.get_object()
        ctx["isFav"] = favourite_books.objects.filter(user_id=self.request.user.id).values_list('book_id', flat=True)
        r = ReadBook.objects.filter(user_id=self.request.user.id).values_list('book_id', flat=True)
        for w in r:
            readlist.append(w)
        ctx["isread"] = readlist
        if RateBook.objects.filter(Q(user_id=self.request.user.id) & Q(book_id=self.get_object().pk)).values_list('rate', flat=True):
            ctx["rateValue"] = range(RateBook.objects.filter(Q(user_id=self.request.user.id) & Q(book_id=self.get_object().pk)).values_list('rate', flat=True)[0])
            ctx["non"] = range(5-RateBook.objects.filter(Q(user_id=self.request.user.id) & Q(book_id=self.get_object().pk)).values_list('rate', flat=True)[0])
        user = self.request.user.id
        try:
            ctx['status'] = wish_list.objects.get(user=user, book=books).status
        except:
            ctx['status'] = False

        return ctx



class AuthorListView(ListView):
    model = Author
    template_name = 'library_view/author_list.html'


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'library_view/author_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        author = self.get_object().pk
        user = self.request.user.id
        try:
            context['status'] = Auth_follow.objects.get(user=user, author=author).status
        except:
            context['status'] = False
        context['mybooks'] = Book.objects.filter(Author=author)
        return context


def CategoryListView(request):
    category_list = Category.objects.all()
    return render(request, 'library_view/category_list.html', {'category_list': category_list})


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'library_view/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['categoryBooks'] = Book.objects.filter(Category=self.kwargs['pk'])
        context['isFav']=FavouriteCategory.objects.filter(user_id=self.request.user.id).values_list('category_id',flat=True)
     
        return context


@login_required
@csrf_exempt
def favourite(request):
    if request.user.is_authenticated:
        id = request.POST.get('id')
        b = favourite_books(user_id=request.user.id, book_id=id)
        b.save()


@login_required
@csrf_exempt
def deleteFav(request):
    if request.user.is_authenticated:
        id=request.POST.get('id')
        favourite_books.objects.filter(Q(user_id=request.user.id) & Q(book_id=id)).delete()


@login_required
@csrf_exempt
def deleteRead(request):
    user = User.objects.get(id=request.user.id)
    book = get_object_or_404(Book, book_id=request.POST['book_id'])
    try:
        ReadBook.objects.get(user=user, book=book).delete()
    except:
        pass
    return redirect('library:BookList')


@login_required
@csrf_exempt
def deleteCat(request):
    if request.user.is_authenticated:
        id = request.POST.get('id')
        FavouriteCategory.objects.filter(Q(user_id=request.user.id) & Q(category_id=id)).delete()



@login_required
@csrf_exempt
def favCat(request):
        if request.method == 'POST':
            if request.user.is_authenticated:
                id = request.POST.get('id')
                b = FavouriteCategory(user_id= request.user.id, category_id=id)
                b.save()


@login_required
@csrf_exempt
def rate(request):
    if request.method == 'POST':
        ratee = request.POST.get('rate')
        id = request.POST.get('id')
        if RateBook.objects.filter(Q(user_id=request.user.id) & Q(book_id=id)):
            RateBook.objects.filter(Q(user_id=request.user.id) & Q(book_id=id)).update(rate=ratee)
        else:
            b = RateBook(user_id= request.user.id,book_id=id,rate=ratee)
            b.save()


@login_required
@csrf_exempt
def read(request):
    user = request.user.id
    book = get_object_or_404(Book, book_id=request.POST['book_id'])
    id = book.pk
    if ReadBook.objects.filter(Q(user_id=user) & Q(book_id=id)):
        pass
    else:
        b = ReadBook(user_id=user, book_id=id)
        b.save()
    try:
        wish_list.objects.get(user=user, book=id, status=True).delete()
    except:
        pass
    book.wishlist.remove(user)
    return redirect('library:BookList')


@login_required
@csrf_exempt
def follow(request):
    user = User.objects.get(id=request.user.id)
    author = get_object_or_404(Author, author_id=request.POST['author_id'])
    try:
        Auth_follow.objects.create(user=user, author=author, status=True)
    except:
        pass
    author.follow.add(user)
    return redirect('library:AuthorList')


@login_required
@csrf_exempt
def unfollow(request):
    user = User.objects.get(id=request.user.id)
    author = get_object_or_404(Author, author_id=request.POST['author_id'])
    try:
        Auth_follow.objects.get(user=user, author=author, status=True).delete()
    except:
        pass
    author.follow.remove(user)

    return redirect('library:AuthorList')


@login_required
@csrf_exempt
def add_to_wishlist(request):
    user = User.objects.get(id=request.user.id)
    book = get_object_or_404(Book, book_id=request.POST['book_id'])
    try:
        wish_list.objects.create(user=user, book=book, status=True)
        ReadBook.objects.get(user=user, book=book).delete()
    except:
        pass
    book.wishlist.add(user)
    return redirect('library:BookList')


@login_required
@csrf_exempt
def remove_from_wishlist(request):
    user = User.objects.get(id=request.user.id)
    book = get_object_or_404(Book, book_id=request.POST['book_id'])
    try:
        wish_list.objects.get(user=user, book=book, status=True).delete()
    except:
        pass
    book.wishlist.remove(user)
    return redirect('library:BookList')
