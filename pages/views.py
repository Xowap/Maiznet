########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> pages/views.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################
from django.template import RequestContext, Template, Context
from django.shortcuts import render_to_response, get_object_or_404
from maiznet.pages.models import Page

def display(request, slug):
	page = get_object_or_404(Page, slug = slug)

	t = Template(page.content)
	c = Context({"user": request.user})

	return render_to_response("pages/display.html", {
		"page": page,
		"content": t.render(c),
	}, RequestContext(request))
