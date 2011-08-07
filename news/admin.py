########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
# Copyright 2011 Grégoire Leroy <gregoire.leroy@retenodus.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################
from maiznet.news.models import News, Category
from django.contrib import admin
from django import forms
from django.core.validators import ValidationError
from django.utils.translation import ugettext as _

class NewsAdminForm(forms.ModelForm):
	class Meta:
		model = News
	
	def clean(self):
		cleaned_data = super(NewsAdminForm, self).clean()
		if cleaned_data["category"].slug == "maintenance" and not self.cleaned_data["date_end"]:
			raise forms.ValidationError(_(u"Le champ date_end n'est pas renseigné"))
		return cleaned_data
class NewsAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug" : ("title",)}
	form = NewsAdminForm

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug" : ("name",)}

admin.site.register(Category,CategoryAdmin)
admin.site.register(News, NewsAdmin)
