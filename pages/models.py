########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> pages/models.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################
from django.db import models

class Page(models.Model):
	title = models.CharField(max_length = 100)
	slug = models.SlugField(unique = True)
	content = models.TextField()

	pub_date = models.DateTimeField(auto_now_add = True)
	mod_date = models.DateTimeField(auto_now = True, auto_now_add = True)
