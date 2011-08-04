from django.template import RequestContext
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from maiznet.register.models import Presence, Room, Promo
from maiznet.register.forms import PresenceForm

def generate_tickets(modeladmin, request, queryset):
	return render_to_response("register/tickets_renew.html", {
		'rooms': queryset,
	}, RequestContext(request))
generate_tickets.short_description = _('Generate tickets')

class RoomAdmin(admin.ModelAdmin):
	actions = [generate_tickets]

class UserProfileInline(admin.StackedInline):
	model = Presence
	form = PresenceForm

class UserProfileAdmin(UserAdmin):
	inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Promo, GroupAdmin)
admin.site.register(Room, RoomAdmin)
