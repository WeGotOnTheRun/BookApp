from django.contrib import admin
from users.models import *
from .views import *
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
