from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from maiznet.register.models import Presence, Room, Promo

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
	model = Presence

class UserProfileAdmin(UserAdmin):
	inlines = [UserProfileInline]

admin.site.register(User, UserProfileAdmin)
admin.site.register(Room)
admin.site.register(Promo, GroupAdmin)
