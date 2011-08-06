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

class NewsAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug" : ("title",)}

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug" : ("name",)}

admin.site.register(Category,CategoryAdmin)
admin.site.register(News, NewsAdmin)
