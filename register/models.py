########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> register/models.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _

class Room(models.Model):
	number = models.CharField(max_length = 20, name = _("room number"), help_text = _("Number of the room, written on the door."))
	ticket = models.CharField(max_length = 14, name = _("ticket"), help_text = _("A unique identifier that was given to you with your key."), unique  = True, blank = True, null = True)

	def __unicode__(self):
		return self.number

class Presence(models.Model):
	user = models.ForeignKey(User, unique = True)
	room = models.ForeignKey(Room, unique = True, blank = True, null = True)
	netif = models.TextField(name = _("network interface"), help_text = ("The MAC adress(es) of your network card. If unsure, keep the pre-filled value"))

	def __unicode__(self):
		if self.room != None:
			return _('Room %(room)s') % {'room': unicode(self.room)}
		else:
			return _('(No room assigned)')

class Promo(Group):
	class Meta:
		ordering = ['name']
