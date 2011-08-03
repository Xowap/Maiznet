########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> monitoring/views.py
#
#
# Copyright 2011 Grégoire Leroy <gregoire.leroy@retenodus.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################

from django.shortcuts import render_to_response
import json

def checkbox(request):
	rfile = open("monitor/state","r")
	strjson = rfile.read()
	services = json.loads(strjson)
	return render_to_response('monitoring/checkbox.html', { 'services' : services })


