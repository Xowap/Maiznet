########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> register/urls.py
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
	url(r'^$', direct_to_template, {'template': 'register/index.html'}, name="register-index"),
	url(r'^signup/$', 'maiznet.register.views.signup', name="register-signup"),
	url(r'^signup/welcome$', direct_to_template, {'template': 'register/welcome.html'}, name="register-welcome"),
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'register/login.html'}, name="login"),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="logout"),
	url(r'^ticket/$', 'maiznet.register.views.ticket', name="register-ticket"),
	url(r'^ticket/done$', direct_to_template, {'template': 'register/changeroom.html'}, name="register-changeroom"),
)
