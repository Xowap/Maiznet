########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> pages/urls.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
# Copyright 2011 Gilles Dehaudt <tonton1728@gmail.com>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################

from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^presence$', 'maiznet.pages.views.presence', name="presence"),
	url(r'^monitoring$','maiznet.pages.views.monitoring', name="monitoring"),
	url(r'^(?P<slug>[-\w]+)$', 'maiznet.pages.views.display', name="page-display"),
)
