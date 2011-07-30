########################################################################
# vim: fileencoding=utf-8 tw=72 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> urls.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################

from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/', include(admin.site.urls)),

	(r'^news/',     include('maiznet.news.urls')),
	(r'^register/', include('maiznet.register.urls')),

	# The index page is actualy the news index page
	(r'^$', redirect_to, {'url': '/news/', 'permanent': True}),
)
