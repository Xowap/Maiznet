########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> register/admin.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################

from django.template import RequestContext
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from maiznet.register.models import Presence, Room, Promo
from maiznet.register.forms import PresenceForm, get_user_promo

def generate_tickets(modeladmin, request, queryset):
	"""
	.. _generation-tickets:

	Vue de l'interface d'administration qui sert à générer les
	tickets. Le template contient un guide de bienvenue à Maiz, en
	plus de l'affichage du ticket.

	Cette vue est appellée par une action dans l'interface
	d'administration, et permet par exemple de générer plusieurs
	tickets à la fois.
	"""
	return render_to_response("register/tickets_renew.html", {
		'rooms': queryset,
	}, RequestContext(request))
generate_tickets.short_description = _('Generate tickets')

class RoomAdmin(admin.ModelAdmin):
	"""
	Administration des chambres.
	"""
	actions = [generate_tickets]
	search_fields = ['number']
	list_per_page = 20
	list_display = ['number', 'ticket']
	ordering = ('number',)

class UserProfileInline(admin.StackedInline):
	"""
	Permet de rajouter la présence en inline sur l'interface
	d'administration des utilisateurs.
	"""
	model = Presence
	form = PresenceForm

class UserProfileAdmin(UserAdmin):
	"""
	Remplace la classe d'admin des utilisateurs par défaut avec une
	classe qui inclue les présences en inline.
	"""
	inlines = [UserProfileInline]
	list_display = ('username', 'room', 'promo', 'email', 'talkings', 'first_name', 'last_name', 'is_staff')
	search_fields = ('username', 'first_name', 'last_name', 'email', 'presence__room__number')

	def room(self, obj):
		return obj.get_profile().room.number
	room.short_description = _('Room')

	def promo(self, obj):
		return get_user_promo(obj)
	promo.short_description = _('Promo')

	def talkings(self, obj):
		return obj.get_profile().talkings
	talkings.short_description = _('Talkings Mailing-List')
	talkings.boolean = True

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Promo, GroupAdmin)
admin.site.register(Room, RoomAdmin)
