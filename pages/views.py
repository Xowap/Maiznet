########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> pages/views.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
# Copyright 2011 Gilles DEHAUDT <tonton1728@gmail.com>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################
from django.template import RequestContext, Template, Context
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext as _
from django.contrib.auth.models import Group
from django.conf import settings
from maiznet.pages.models import Page

def display(request, slug):
	"""
	Affiche une page.

	Avant l'affichage, le contenu de la page est passé au moteur de
	rendu de template, au cas où la page aurait besoin de certaines
	fonctions, comme par exemple la génération d'URL.
	"""
	page = get_object_or_404(Page, slug = slug)

	t = Template(page.content)
	c = RequestContext(request)

	return render_to_response("pages/display.html", {
		"page": page,
		"content": t.render(c),
	}, RequestContext(request))

def presence(request) :
	"""
	Affiche les admins presents a Maiz
	"""

	admins = Group.objects.get(id=settings.ADMIN_GROUP_ID).user_set.exclude(presence__room__isnull = True)

	return render_to_response("pages/presence.html", {
		"admins": admins,
	}, RequestContext(request))
