########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> pages/admin.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from maiznet.pages.models import Page

class PageAdmin(TranslationAdmin):
	list_display = ['title', 'slug', 'pub_date', 'mod_date']
	prepopulated_fields = {"slug": ("title",)}

admin.site.register(Page, PageAdmin)
