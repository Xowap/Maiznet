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

import config
import socket
from sqlite3 import dbapi2 as sqlite
from datetime import datetime, timedelta

class MonitorProtocol(object):
	"""
	Je gère le protocole de Monitor. Je prend en paramètre l'adresse IP et le port auxquels me connecter.
	"""
	def __init__(self):
		self.ip_server = config.IP_MUNIN
		self.port = config.PORT_MUNIN

	def fetchValue(self, plugin):
		"""
			Communication avec Monitor-node pour récupérer les valeurs mesurées par un plugin.
		"""
		values = []

		# Création du socket et connexion
		try : 
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.settimeout(3)
			s.connect((self.ip_server,self.port))
		except :
			raise Exception("Échec de l'établisement de la connexion")
		try :
			data = s.recv(4096)
		except :
			raise Exception("Échec de la connexion")

		# Lors de l'établissement d'une connection, Monitor envoie toujours "# Munin node at [host]"
		if "# munin node at" not in data :
			raise Exception("Mauvaises données reçues")

		# Le protocole Munin contient la commande fetch qui permet de récupérer des données
		s.send("fetch %s \r\n" % plugin)
		try : 
			# La fin de la sortie d'une commande se termine toujours par "\n.\n"
			while "\n.\n" not in data :
				data = s.recv(4096)
				data_t = data.split("\n")[0].split(" ")[1]
				values.append(data_t)
		except :
			Exception("No data received")
		s.send("quit\n")
		s.close()
		return values
