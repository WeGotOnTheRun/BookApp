from . import views
from django.urls import path, re_path


app_name = 'community'

urlpatterns = [
    path('community/', views.home, name='home'),
    path('savequestion/', views.savequestion, name='savequestion'),
    re_path(r'^saveanswer/(?P<questionid>[0-9]+)$', views.saveanswer, name='saveanswer'),
]
