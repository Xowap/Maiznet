from maiznet.news.models import News, Category
from django.contrib import admin

class NewsAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug" : ("title",)}
admin.site.register(Category)
admin.site.register(News, NewsAdmin)
