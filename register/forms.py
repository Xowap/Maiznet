########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> register/forms.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################

from django.conf import settings
from django.forms import Form, ModelForm, RegexField, ModelChoiceField, CharField, EmailField, ValidationError, BooleanField
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from maiznet.register.models import Presence, Promo, Room
from maiznet.register.fields import MacAddressField
from maiznet.register.tipmac import ip_to_mac

def validate_ticket(value):
	# Vérifie le format
	import re
	r = re.compile(r"^\d{4}-\d{4}-\d{4}$")
	if r.match(value) == None:
		raise ValidationError(_("The ticket should be formated like xxxx-xxxx-xxxx, with x being a digit"))

	# Vérifie la validité du ticket
	try:
		Room.objects.get(ticket = value)
	except Room.DoesNotExist:
		raise ValidationError(_("No room exists with this ticket"))

def validate_mac(value, presence=None):
	if value == "":
		return

	if isinstance(presence, Presence):
		qs = Presence.objects.exclude(pk=presence.pk)
	else:
		qs = Presence.objects

	macs = value.split(",")

	if len(macs) > 30:
		raise ValidationError(_('You cannot register more than 30 MAC addresses'))

	for mac in macs:
		if qs.filter(netif__contains=mac).count() > 0:
			raise ValidationError(_('Somebody is already using the MAC address %(mac)s') % {'mac': mac})

def get_user_promo(user):
	promo = None
	for group in user.groups.all():
		try:
			promo = Promo.objects.get(pk = group.pk)
			break
		except Promo.DoesNotExist:
			pass

	return promo

class TicketForm(Form):
	ticket = CharField(max_length = 14, validators = [validate_ticket])

	def save(self, user):
		# La chambre de l'utilisateur
		room = Room.objects.get(ticket = self.cleaned_data["ticket"])

		# En cas d'occupant précédent, on l'enlève de la chambre
		try:
			prev = Presence.objects.get(room = room)
			prev.room = None
			prev.save()
		except Presence.DoesNotExist:
			pass

		# On modifie son profil
		try:
			p = user.get_profile()
		except Presence.DoesNotExist:
			p = Presence(user = user)
		p.room = room
		p.save()

class PresenceForm(ModelForm):
	netif = MacAddressField(label = _("MAC Address"), help_text = _("This is the MAC address of your network card. If unsure, keep the default value."), required = False)

	class Meta:
		model = Presence

	def clean_netif(self):
		netif = self.cleaned_data["netif"]
		validate_mac(netif, self.instance)
		return netif

class UserRegistrationForm(UserCreationForm):
	username   = RegexField(label = _("Username"), max_length = 30, regex = r'^[a-zA-Z][a-zA-Z0-9\-_]+[a-zA-Z]$',
		help_text = _("Required. 30 characters or fewer. Begins and ends with a letter and can contain letters, digits, _ and -."),
		error_messages = {'invalid': _("This value must begin and end with a letter and can contain letters, digits, and _/-")})
	first_name = CharField(label = _("Firstname"), max_length = 30)
	last_name  = CharField(label = _("Lastname"), max_length = 30)
	email      = EmailField(label = _("Email"), help_text=_("This email address is used by Maiz and Maiznet for official announces. You really should enter an address you use often. Please don't use hotmail or live addresses as our mails are considered as SPAM."))
	promo      = ModelChoiceField(label = _("Promo"), help_text = _('Your promo'), queryset = Promo.objects.all(), empty_label = _("(None)"), required = False)
	ticket     = CharField(max_length = 14, validators = [validate_ticket])
	netif      = MacAddressField(label = _("MAC Address"), help_text = _("This is the MAC address of your network card. If unsure, keep the default value."), validators = [validate_mac], required = False)
	talkings   = BooleanField(required = False, label = _("Subscribe to the talkings mailing-list"), help_text = _("Whatever you choose, you will subscribe to the Maiznet and Maiz announces mailing-list. The talkings mailing-list is the maling-list between inhabitants of Maiz. You should let this check-in"))

	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "email")

	def clean_email(self):
		email = self.cleaned_data["email"]

		if len(User.objects.filter(email = email)) > 0:
			raise ValidationError(_("A user with that email already exists."))

		return email

	def clean_password2(self):
		p = super(UserRegistrationForm, self).clean_password2()
		if len(p) > 61:
			raise ValidationError(_("Your password should not be longer than 61 characters"))
		return p

	def save(self):
		user = super(UserRegistrationForm, self).save()

		# La chambre de l'utilisateur
		room = Room.objects.get(ticket = self.cleaned_data["ticket"])

		# En cas d'occupant précédent, on l'enlève de la chambre
		try:
			prev = Presence.objects.get(room = room)
			prev.room = None
			prev.save()
		except Presence.DoesNotExist:
			pass

		# On créé son profil
		p = Presence(user = user, room = room, netif = self.cleaned_data["netif"], talkings = self.cleaned_data["talkings"])
		p.save()

		# On l'ajoute à sa promo
		if self.cleaned_data['promo'] != None:
			user.groups.add(self.cleaned_data["promo"])

		return user

class UserModificationForm(ModelForm):
	first_name = CharField(label = _("Firstname"), max_length = 30)
	last_name  = CharField(label = _("Lastname"), max_length = 30)
	email      = EmailField(label = _("Email"), help_text=_("This email address is used by Maiz and Maiznet for official announces. You really should enter an address you use often. Please don't use hotmail or live addresses as our mails are considered as SPAM."))
	promo = ModelChoiceField(label = _("Promo"), help_text = _('Your promo'), queryset = Promo.objects.all(), empty_label = _("(None)"), required = False)
	netif = MacAddressField(label = _("MAC Address"), help_text = _("This is the MAC address of your network card. If unsure, keep the default value. If you are using a new mac address, it has been added to the list, but you should still save."), required = False)
	talkings   = BooleanField(required = False, label = _("Subscribe to the talkings mailing-list"), help_text = _("Whatever you choose, you will subscribe to the Maiznet and Maiz announces mailing-list. The talkings mailing-list is the maling-list between inhabitants of Maiz. You should let this check-in"))

	class Meta:
		model = User
		fields = ("id", "first_name", "last_name", "email")

	def __init__(self, data = None, files = None, instance = None, initial = None, remote_ip = None, *args, **kwargs):
		if instance != None:
			if initial == None:
				initial = {}

			# Il faut deviner la promo
			initial['promo'] = get_user_promo(instance)

			try:
				p = instance.get_profile()
			except Presence.DoesNotExist:
				p = Presence(user = instance)

			netif = p.netif
			try:
				mac = ip_to_mac(remote_ip)
				if netif.find(mac) == -1:
					if netif != '':
						netif += ','
					netif += mac
			except:
				pass

			initial['netif'] = netif
			initial['talkings'] = p.talkings

		super(UserModificationForm, self).__init__(data = data, files = files, instance = instance, initial = initial, *args, **kwargs)

	def clean_email(self):
		email = self.cleaned_data["email"]

		if self.instance == None or self.instance.email != email:
			if User.objects.filter(email = email).count() > 0:
				raise ValidationError(_("A user with that email already exists."))

		return email

	def clean_netif(self):
		netif = self.cleaned_data["netif"]
		try:
			validate_mac(netif, self.instance.get_profile())
		except Presence.DoesNotExist:
			validate_mac(netif)
		return netif

	def save(self):
		user = super(UserModificationForm, self).save()

		# Est-ce que l'utilisateur a changé de promo ?
		promo = get_user_promo(user)
		if promo != self.cleaned_data['promo']:
			user.groups.remove(promo)

			if self.cleaned_data['promo'] != None:
				user.groups.add(self.cleaned_data['promo'])

		# Et on met à jour sa carte réseau
		p = user.get_profile()
		p.netif = self.cleaned_data['netif']
		p.talkings = self.cleaned_data['talkings']
		p.save()

		return user
