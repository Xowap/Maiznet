########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> new/views.py
#
#
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################

from datetime import datetime, timedelta
from maiznet.news.models import New
from django.shortcuts import render_to_response
from django.db.models import Q

def print_news(request):
	news = New.objects.filter(
		date_start__lte = datetime.now() + timedelta(days=3),
		date_end__gte =  datetime.now() - timedelta(hours=2)
	)[0:20]
	print news
	return render_to_response('news/index.html', { 'news' : news })
