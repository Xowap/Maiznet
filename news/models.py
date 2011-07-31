########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> new/models.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################
from django.db import models
from django.utils.translation import ugettext as _
from datetime import datetime

class Category(models.Model):
	name = models.CharField(max_length = 40)

	def __unicode__(self):
		return self.name
	
	class Meta:
		verbose_name_plural = "Categories"

class News(models.Model):
	title = models.CharField(max_length = 40)
	content = models.TextField(max_length = 140)
	category = models.ForeignKey(Category)
	date_start = models.DateTimeField(default = datetime.now, blank = True)
	date_end = models.DateTimeField(blank = True, null = True, default = None)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ["-date_start"]
		verbose_name_plural = "News"
