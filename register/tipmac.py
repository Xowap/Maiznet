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
	Retourne True si la valeur est une adresse MAC, False sinon.
	"""

	X = '([a-fA-F0-9]{2}[:\-]){5}[a-fA-F0-9]{2}' # this is the regex
	if re.compile(X).search(mac):
		return True
	return False

def ip_to_mac(ip):
	"""
	Effectue une requête auprès du serveur tipmac, et retourne la
	MAC correspondant à l'IP. Si la MAC est incorrecte, une
	exception est levée.

	Cette fonction dépend de paramètres à définir dans le
	settings.py :

	  - **MAIZ_IP_GUEST**, la plage d'IP des invités. Si l'adresse
	    n'est pas dans cette plage, la fonction retourne tout de
	    suite une exception. À l'heure où ces lignes sont écrites,
	    cette plage est 172.17.192.0/18.
	  - **TIPMAC_SERVER**, l'adresse IP du serveur tipmac.
	  - **TIPMAC_PORT**, le port du serveur.
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
