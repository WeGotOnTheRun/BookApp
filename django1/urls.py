from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from library import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('', include('library.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('library/books/love/', views.favourite, name='favourite'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
