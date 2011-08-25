########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> register/views.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from maiznet.register.forms import UserRegistrationForm, UserModificationForm, TicketForm
from maiznet.register.models import Promo, Presence
from maiznet.register.tipmac import ip_to_mac
from maiznet.register.decorators import anonymous_required

@anonymous_required
def signup(request):
	"""
	Affiche le formulaire d'enregistrement, et si la requête est de
	type POST, valide le formulaire puis l'enregistre.

	La vue se charge aussi de pré-remplir certaines valeurs, comme
	la promo (si l'utilisateur n'est pas encore inscrit, il est
	probablement dans la promo la plus récente), et l'adresse MAC
	(en faisant appel à l'outil :ref:`tipmac <intro-tipmac>`)
	"""
	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			user = authenticate(username = form.cleaned_data['username'], password = request.POST['password1'])
			login(request, user)
			return redirect('register-welcome')
	else:
		try:
			promo = Promo.objects.filter(name__startswith = 'FI').order_by('-name')[0]
		except:
			promo = None

		try:
			mac = ip_to_mac(request.META['REMOTE_ADDR'])
		except:
			mac = None

		form = UserRegistrationForm(initial = {
			'netif': mac,
			'promo': promo
		})

	return render_to_response("register/signup.html", {
		"form": form,
	}, RequestContext(request))

@login_required
def edit(request):
	"""
	Permet l'édition du profil utilisateur.
	"""

	if request.method == "POST":
		form = UserModificationForm(data = request.POST, instance = request.user)
		if form.is_valid():
			form.save()
			return redirect('register-edit-done')
	else:
		form = UserModificationForm(instance = request.user, remote_ip = request.META['REMOTE_ADDR'])

	return render_to_response("register/edit.html", {
		"form": form,
	}, RequestContext(request))

@login_required
def welcome(request):
	"""
	Affiche un message de bienvenue à l'utilisateur, une fois qu'il
	a réussi son inscription.
	"""
	return render_to_response("register/welcome.html", {}, RequestContext(request))

@login_required
def ticket(request):
	"""
	Permet à l'utilisateur de saisir un nouveau ticket et de le
	valider.
	"""
	if request.method == "POST":
		form = TicketForm(request.POST)
		if form.is_valid():
			form.save(request.user)
			return redirect('register-changeroom')
	else:
		form = TicketForm()

	return render_to_response("register/ticket.html", {
		"form": form,
	}, RequestContext(request))

@login_required
def quit(request, do = None):
	"""
	Libère la chambre, pour quand un utilisateur décide de quitter
	Maiz. À priori, c'est **la** fonction qui ne va jamais servir.
	"""
	if do == "do":
		try:
			p = request.user.get_profile()
			p.room = None
			p.save()
		except Presence.DoesNotExist:
			pass

		return render_to_response("register/quit_done.html", {}, RequestContext(request))

	return render_to_response("register/quit_ask.html", {}, RequestContext(request))
