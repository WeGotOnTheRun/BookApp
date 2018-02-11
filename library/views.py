from .models import *
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView


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
