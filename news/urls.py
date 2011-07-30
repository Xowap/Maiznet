########################################################################
# vim: fileencoding=utf-8 tw=72 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> news/urls.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
	url(r'^$', direct_to_template, {'template': 'news/index.html'},
	    name="news-index"),
)
