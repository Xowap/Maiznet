########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> register/decorators.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################

from django.http import HttpResponseRedirect
from functools import wraps

def anonymous_required(f, redirect_to = '/'):
	"""
	Si l'utilisateur est authentifié, on le redirige vers une autre
	page ('/' par défaut).
	"""
	@wraps(f)
	def wrapper(request, *args, **kwargs):
		if request.user.is_authenticated():
			return HttpResponseRedirect(redirect_to)
		return f(request, *args, **kwargs)
	return wrapper
