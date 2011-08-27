########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> translation.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################
from modeltranslation.translator import translator, TranslationOptions
from maiznet.pages.models import Page

class PageTranslationOptions(TranslationOptions):
	"""
	Indique à modeltranslation de traduire les pages.
	"""
	fields = ('title', 'content')

translator.register(Page, PageTranslationOptions)
