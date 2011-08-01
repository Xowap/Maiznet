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
from maiznet.register.forms import UserRegistrationForm, TicketForm
from maiznet.register.models import Promo

# TODO faire une vraie fonction
def ip_to_mac(ip):
	print ip
	return '00:1f:16:b6:9a:ac'

def signup(request):
	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('register-welcome')
	else:
		try:
			promo = Promo.objects.filter(name__startswith = 'FI').order_by('-name')[0]
		except:
			promo = None

		form = UserRegistrationForm(initial = {
			'netif': ip_to_mac(request.META['REMOTE_ADDR']),
			'promo': promo
		})

	return render_to_response("register/signup.html", {
		"form": form,
	}, RequestContext(request))

@login_required
def ticket(request):
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
