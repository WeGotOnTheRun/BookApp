from django.urls import path, re_path,include
from . import views

app_name = 'library'

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),

    path('books/', views.BookListView.as_view(), name='BookList'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='BookDetail'),



    re_path(r'^books/love/',views.favourite, name='favourite'),
    re_path(r'^hello/(?P<id>[0-9]+)/',views.hello, name='favBook'),
    re_path(r'^rate',views.rate, name='rate'),
    re_path(r'^read',views.read, name='read'),
    re_path(r'^favCat',views.favCat, name='favCat'),

    path('authors/', views.AuthorListView.as_view(), name='AuthorList'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='AuthorDetail'),


    path('categories/', views.CategoryListView, name='CategoryList'),
    path('categories/<int:pk>',views.CategoryDetailView.as_view(), name='CategoryDetail'),

]
