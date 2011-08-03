########################################################################
# vim: fileencoding=utf-8 ts=8 noexpandtab :
#
# ~~~~ Maiznet.fr ~~~~
#
#  -> register/tipmac.py
#
#
# Copyright 2011 Grégoire Leroy <gregoire.leroy@retenodus.net>
# Copyright 2011 Rémy Sanchez <remy.sanchez@hyperthese.net>
#
# This file is distributed under the terms of the WTFPL. For more
# informations, see http://sam.zoy.org/wtfpl/COPYING
########################################################################

import socket
import re
from django.conf import settings

def isMac(mac):
	"""
	Return True if the string 'mac' is a MAC address, False else.
	"""

	X = '([a-fA-F0-9]{2}[:\-]){5}[a-fA-F0-9]{2}' # this is the regex
	if re.compile(X).search(mac):
		return True
	return False

def ip_to_mac(ip):
	"""
	Return the MAC address given by remote host, if it's valid
	"""

	# Teste si l'adresse IP est un invité de Maiz
	import IPy
	if ip == None or IPy.IPint(settings.MAIZ_IP_GUEST).overlaps(ip) != 1:
		raise Exception("IP not in guest subnet")

	ip_server = settings.TIPMAC_SERVER
	port = settings.TIPMAC_PORT

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(3)
	s.connect((ip_server,port))
	s.send(ip)

	try :
		mac = s.recv(17)
	except :
		raise Exception("No data received")
	if not isMac(mac):
		raise Exception("Error : invalid MAC")

	s.close()
	return mac
