#!/usr/bin/python

from django.core.management import setup_environ
import sys

sys.path.append('/var/wsgi/maiznet2')
sys.path.append('/var/wsgi')

from maiznet import settings

setup_environ(settings)

from maiznet.register.models import Presence

wfile_announces = open("/var/wsgi/maiznet2/maiznet/tools/ml/emails_announces","w")
wfile_talkings = open("/var/wsgi/maiznet2/maiznet/tools/ml/emails_talkings","w")
presence = Presence.objects.all()

for p in presence :
	if p.talkings=1 :
		wfile_talkings.write(p.user.email + "\n")
	wfile_announces.write(p.user.email + "\n")

wfile_announces.close()
wfile_talkings.close()
