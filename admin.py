from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from spistresci.blogger.models import BloggerProfile, BookRecommendation


class UserAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ('date_joined', 'last_login')

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
from django.contrib import admin
admin.site.register(BloggerProfile)
admin.site.register(BookRecommendation)
