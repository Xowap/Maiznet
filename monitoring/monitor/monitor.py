#-*- coding:utf-8 -*-
import socket
from sqlite3 import dbapi2 as sqlite
from datetime import datetime, timedelta
import os

relpath = os.path.dirname(os.path.realpath(__file__))

class MonitorProtocol(object):
	"""
	Je gère le protocole de Monitor. Je prend en paramètre l'adresse IP et le port auxquels me connecter.
	"""
	def __init__(self,port=4949,ip_server="192.168.0.1",basepath):
		self.ip_server = ip_server
		self.port = port
		self.connection = sqlite.connect(basepath)
		self.cursor = self.connection.cursor()

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
		s.send("fetch " + plugin + '\r\n')
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

	def commitDB(self):
		self.connection.commit()
		

	def closeDB(self):
		self.connection.commit()
		self.connection.close()
		
class MonitorPlugin(object):
	def __init__(self,plugin,monitorprotocol):
		self.plugin = plugin
		self.mp = monitorprotocol
	

	def fetchValue(self, function = lambda values : values):
		"""
		Récupère et modifie éventuellement les valeurs
		"""
		self.values = self.mp.fetchValue(self.plugin)
		self.values = function(self.values)
	
	def insertValues(self):
		"""
		Insère les valeurs dans la base de données
		"""
		week = (datetime.now() - timedelta(days=7),)
		hours = (datetime.now() - timedelta(hours=2),)
		now = (datetime.now(),)
		self.mp.cursor.execute('INSERT INTO ' + self.plugin + ' VALUES (null, "' + '", "'.join(self.values) + '", datetime(?))',(now))
		self.mp.cursor.execute('DELETE FROM ' + self.plugin + ' WHERE datetime(date) <  datetime(?)', hours)
	
	def retreiveValues(self):
		""" Utilisé pour les tests uniquement """
		self.mp.cursor.execute('SELECT * FROM if_re1')

def ifacePluginDB(names,basepath = "/root/monitor/monitor.db"):
	connection = sqlite.connect(basepath)
	cursor = connection.cursor()
	for name in names :
		cursor.execute('CREATE TABLE ' + name + ' (id INTEGER PRIMARY KEY, `in` INTEGER, out INTEGER, date DATETIME)')
	connection.commit()
	connection.close()

# La ligne suivante ne doit être décommentée que s'il faut réinstalle la bdd
#ifacePluginDB(["if_re1","if_re2","if_re3"])
ifaceplugins = ["if_re1","if_re2","if_re3"]
mprot = MonitorProtocol()
for plugin in ifaceplugins :
	mplug = MonitorPlugin(plugin,mprot,relpath+"/monitor.db")
	mplug.fetchValue(function= lambda values : [str(int(value)/1024) for value in values])
	mplug.insertValues()
	mprot.commitDB()
#mplug.retreiveValues()
mprot.closeDB()
