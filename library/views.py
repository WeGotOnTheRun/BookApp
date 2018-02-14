from .models import *
from users.models import *
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View

from django.views.decorators.csrf import csrf_exempt
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
        ctx["book"]=self.get_object()
        ctx["isFav"]=favourite_books.objects.filter(user_id=self.request.user.id).values_list('book_id',flat=True)
        return ctx

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        book = self.get_object().pk
        context['categoryBooks'] = Book.objects.get(pk=book).Category.all()
        return context


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
        return context

def favourite(request):
    user=request.user
    # user.favourite_books.add(Book)
    return JsonResponse(1,safe=False)




@login_required
def hello(request,id):
    b=favourite_books(user_id= request.user.id,book_id=id)
    b.save()


@login_required
@csrf_exempt
def rate(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        ratee = request.POST.get('rate')
        id=request.POST.get('id')
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


@login_required
@csrf_exempt
def favCat(request):
    if request.method == 'GET':
            pass
    elif request.method == 'POST':
        id=request.POST.get('id')
        b=FavouriteCategory(user_id= request.user.id,category_id=id)
        b.save();
        return HttpResponse("sdj")
