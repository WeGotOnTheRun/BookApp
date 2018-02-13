from django.contrib import admin
from users.models import *
from .views import *
from .models import *


class ExtendUser(admin.StackedInline):
    model = Profile
    can_delete = False
    Verbose_name = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ExtendUser,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
