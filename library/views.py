from .models import *
from users.models import *
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
def index(request):
    books = Book.objects.all().order_by('-book_id')[:3]
    authors = Author.objects.all()[:3]
    categories = Category.objects.all()[:3]
    return render(request, 'library_view/index.html', {'books': books, 'authors': authors, 'categories': categories})


class BookListView(ListView):
    model = Book
    template_name = 'library_view/book_list.html'


class BookDetailView(DetailView):
    model = Book
    template_name = 'library_view/book_detail.html'
    def get_context_data(self, *args, **kwargs):
        ctx =super(BookDetailView, self).get_context_data(*args, **kwargs)
        books = self.get_object().pk
        ctx['categoryBooks'] = Book.objects.get(pk=books).Category.all()
        ctx["book"]=self.get_object()
        ctx["isFav"]=favourite_books.objects.filter(user_id=self.request.user.id).values_list('book_id',flat=True)
        if RateBook.objects.filter(Q(user_id=self.request.user.id) & Q(book_id=self.get_object().pk)).values_list('rate', flat=True):
            ctx["rateValue"]=range(RateBook.objects.filter(Q(user_id=self.request.user.id) & Q(book_id=self.get_object().pk)).values_list('rate', flat=True)[0])
            ctx["non"]=range(5-RateBook.objects.filter(Q(user_id=self.request.user.id) & Q(book_id=self.get_object().pk)).values_list('rate', flat=True)[0])
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
        context['mybooks'] = Book.objects.filter(Author=author)
        return context


def CategoryListView(request):
    category_list = Category.objects.all()
    return render(request, 'library_view/category_list.html', {'category_list': category_list})

class CategoryDetailView(DetailView):
    model=Category
    template_name = 'library_view/category_detail.html'
    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['categoryBooks'] = Book.objects.filter(Category=self.kwargs['pk'])
        context['isFav']=FavouriteCategory.objects.filter(user_id=self.request.user.id).values_list('category_id',flat=True)
        return context

@csrf_exempt
def favourite(request):
    if request.user.is_authenticated:
        id=request.POST.get('id')
        b=favourite_books(user_id= request.user.id,book_id=id)
        b.save()
        return HttpResponse("insert")


@csrf_exempt
def deleteFav(request):
    if request.user.is_authenticated:
        id=request.POST.get('id')
        favourite_books.objects.filter(Q(user_id=request.user.id) & Q(book_id=id)).delete()
        return HttpResponse("Done deleted")

@csrf_exempt
def deleteRead(request):
    if request.user.is_authenticated:
        id=request.POST.get('id')
        ReadBook.objects.filter(Q(user_id=request.user.id) & Q(book_id=id)).delete()
        return HttpResponse("Done deleted")

@csrf_exempt
def deleteCat(request):
    if request.user.is_authenticated:
        id=request.POST.get('id')
        FavouriteCategory.objects.filter(Q(user_id=request.user.id) & Q(category_id=id)).delete()
        return HttpResponse("Done deleted")



@csrf_exempt
def favCat(request):
        if request.method == 'POST':
            if request.user.is_authenticated:
                id=request.POST.get('id')
                b=FavouriteCategory(user_id= request.user.id,category_id=id)
                b.save();
            else:
                return HttpResponse("login_required")


@login_required
@csrf_exempt
def rate(request):
    if  request.method == 'POST':
        ratee = request.POST.get('rate')
        id=request.POST.get('id')
        if(RateBook.objects.filter(Q(user_id=request.user.id) & Q(book_id=id))):
            RateBook.objects.filter(Q(user_id=request.user.id) & Q(book_id=id)).update(rate=ratee)
        else:
            b=RateBook(user_id= request.user.id,book_id=id,rate=ratee)
            b.save();

@login_required
@csrf_exempt
def read(request):
    if request.method == 'GET':
            pass
    elif request.method == 'POST':
        id=request.POST.get('id')
        b=ReadBook(user_id= request.user.id,book_id=id)
        b.save();
        return HttpResponse("Read")


