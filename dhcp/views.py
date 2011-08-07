########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> dhcp/views.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################

import IPy
from django.shortcuts import render_to_response, redirect
from maiznet.register.models import Presence
from django.template import RequestContext
from django.conf import settings

def conf(request):
	ip = request.META['REMOTE_ADDR']
	if IPy.IPint(settings.MAIZ_DHCP_REQUESTER).overlaps(ip) != 1:
		return redirect('/')

	return render_to_response("dhcp/dhcpd.conf", {
		'presences': Presence.objects.exclude(room__isnull=True)
	}, RequestContext(request))
