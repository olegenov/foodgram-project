from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class UserAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ('first_name', 'email')
    search_fields = UserAdmin.search_fields + ('first_name', 'email')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
