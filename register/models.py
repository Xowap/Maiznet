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

# Hacks
# Ça sert à avoir une authentification insensible à la casse. On ne pose
# pas de questions, merci.

_tmp = User.objects.get
def hack_user_get(*args, **kwargs):
	if 'username' in kwargs:
		kwargs['username__iexact'] = kwargs.pop('username')

	return _tmp(*args, **kwargs)
User.objects.get = hack_user_get

# Là ça sert à avoir des mots de passe stockés en quasi-cleartext...
# C'est pas une bonne idée je sais, un jour faudra faire mieux, mais là
# c'est la moins pire qu'on ait pour pouvoir brancher sur la base des
# services inconnus dont on ne sait pas s'ils vont gérer ce hash là en
# particulier ou pas.

from django.utils.encoding import smart_str
import django.contrib.auth.models

# Encodage d'une chaîne en hexadeciman
def _hexstr(s):
	return "".join([hex(ord(x))[2:] for x in smart_str(s)]).upper()

# Remplacement pour la méthode de hashage
def _hack_set_password(self, raw_password):
	self.password = 'maiz$$%s' % _hexstr(raw_password)
User.set_password = _hack_set_password

# Remplacement pour la méthode de vérification du hash
_orig_get_hexdigest = django.contrib.auth.models.get_hexdigest
def _hack_get_hexdigest(algorithm, salt, raw_password):
	if algorithm == 'maiz':
		return _hexstr(raw_password)
	else:
		return _orig_get_hexdigest(algorithm, salt, raw_password)
django.contrib.auth.models.get_hexdigest = _hack_get_hexdigest
