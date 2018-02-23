from django.urls import path, re_path,include
from . import views
app_name = 'library'
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),

    path('books/', views.BookListView.as_view(), name='BookList'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='BookDetail'),

    path('authors/', views.AuthorListView.as_view(), name='AuthorList'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='AuthorDetail'),

    path('categories/', views.CategoryListView, name='CategoryList'),
    path('categories/<int:pk>', views.CategoryDetailView.as_view(), name='CategoryDetail'),

    path('follow/', views.follow, name="follow"),
    path('unfollow/', views.unfollow, name="unfollow"),

    path('add_to_wishlist/', views.add_to_wishlist, name="add_to_wishlist"),
    path('remove_from_wishlist/', views.remove_from_wishlist, name="remove_from_wishlist"),

    re_path(r'^favourite', views.favourite, name='favBook'),
    re_path(r'^delFav', views.deleteFav, name='delfavBook'),
    re_path(r'^deleteRead', views.deleteRead, name='delreadBook'),
    re_path(r'^rate', views.rate, name='rate'),
    path('read/', views.read, name='read'),
    path('unread/', views.deleteRead, name='deleteRead'),
    re_path(r'^favCat', views.favCat, name='favCat'),
    re_path(r'^delCat', views.deleteCat, name='delCat'),

]
