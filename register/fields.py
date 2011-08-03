########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> register/fields.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################

from django.forms import RegexField

class MacAddressField(RegexField):
	def __init__(self, *args, **kwargs):
		super(MacAddressField, self).__init__(regex = r'^(([0-9a-f]{2}:){5}[0-9a-f]{2},)*([0-9a-f]{2}:){5}[0-9a-f]{2}$', *args, **kwargs)

	def clean(self, value):
		value = value.replace(" ", "").replace("-", ":").lower()
		return super(MacAddressField, self).clean(value)
