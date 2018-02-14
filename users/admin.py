from django.contrib import admin
from users.models import *

admin.site.register(Profile)
admin.site.register(favourite_books)
admin.site.register(RateBook)
admin.site.register(ReadBook)
admin.site.register(FavouriteCategory)