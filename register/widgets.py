########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> register/widgets.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################

from django.forms.widgets import TextInput

class MacInput(TextInput):
	class Media:
		js = ('static/js/widget-mac.js',)

	def render(self, name, value, attrs=None):
		cls = ['maiz-input-widget']

		try:
			cls.append(attrs['class'])
		except TypeError:
			attrs = {}
		except:
			pass

		attrs['class'] = ' '.join(cls)

		return super(MacInput, self).render(name, value, attrs)
