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

def anonymous_required(view_func, redirect_to = '/'):
	def _wrapped_view(request, *args, **kwargs):
		if request.user.is_authenticated():
			return HttpResponseRedirect(redirect_to)
		return view_func(request, *args, **kwargs)
	return _wrapped_view
