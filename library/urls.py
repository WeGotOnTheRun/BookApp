from django.urls import path, re_path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.index, name='index'),

    path('books/', views.BookListView.as_view(), name='BookList'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='BookDetail'),

    path('authors/', views.AuthorListView.as_view(), name='AuthorList'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='AuthorDetail'),

    path('categories/', views.CategoryListView, name='CategoryList'),
    # re_path(r'^categories/(?P<category_id>[0-9]+)$', views.CategoryDetailView, name='CategoryDetail'),

]
