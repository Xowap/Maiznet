from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from maiznet.register.models import Presence, Room

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
	model = Presence

class UserProfileAdmin(UserAdmin):
	inlines = [UserProfileInline]

admin.site.register(User, UserProfileAdmin)
admin.site.register(Room)
