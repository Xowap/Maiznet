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
from maiznet.register.forms import PresenceForm

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

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Promo, GroupAdmin)
admin.site.register(Room, RoomAdmin)
