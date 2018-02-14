from django.urls import path, re_path, include
from . import views
from django.contrib.auth import views as view


urlpatterns = [
    re_path(r'^signup/$', views.sign_up, name='signup'),  # signup.
    re_path(r'^$', views.home, name='home'),
    re_path(r'^login/$', view.login, {'template_name': 'login.html'}, name='login'),
    re_path('logout', view.logout, {'next_page': 'login'}, name='logout'),
    re_path(r'^search', views.search, name='search'),
]
