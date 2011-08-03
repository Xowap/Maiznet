########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> new/views.py
#
#
# Copyright 2011 Grégoire Leroy <gregoire.leroy@retenodus.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################

from datetime import datetime, timedelta
from maiznet.news.models import News
from django.shortcuts import render_to_response
from django.db.models import Q
from django.template import RequestContext

def print_news(request):
	news = News.objects.filter(
		Q(date_end__gte =  datetime.now() - timedelta(hours=2)) | Q(date_end = None),
		date_start__lte = datetime.now() + timedelta(days=3)
	)[0:20]
	return render_to_response('news/index.html', { 'news' : news },context_instance=RequestContext(request))
