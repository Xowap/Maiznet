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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sg_filter
from sqlite3 import dbapi2 as sqlite
from strdate import parseDateTime  
import datetime

class MonitorGraph(object):
	"""
	Je trace le graphe
	"""
	def __init__(self,plugin):
		self.connection = sqlite.connect(config.DATABASE)
		self.cursor = self.connection.cursor()
		self.plugin = plugin
		self.now = datetime.datetime.now()
		self.coeff = sg_filter.calc_coeff(config.LISSAGE_NUM_POINTS,config.LISSAGE_COEFF)
	
	def getData(self):
		"""
		Récupère les données de la base de données
		"""
		self.cursor.execute("SELECT * FROM %s ORDER BY date DESC" self.plugin) 
		self.data = self.cursor.fetchall()
	
	def positionToSpeed(self):
		"""
		Calcule une liste de vitesse depuis une liste de positions
		"""
		self.speed = []

		for data in self.data:
			if self.data.index(data) == 0:
				continue
			d = self.data[self.data.index(data)-1]
			if d[1] < data[1] or d[2] < data[2]:
				continue
			date1 = parseDateTime(str(d[3]))
			date2 = parseDateTime(str(data[3]))
			times = (date1-date2).seconds
			
			self.speed.append([
				(d[1] - data[1])/times,
				(d[2] - data[2])/times,
				(datetime.datetime.now()-date1).seconds/60
				
			])

	def gen_picture(file_,width,decoration):
		"""
		Génère une image
		"""

		times = [speed[2] for speed in self.speed]

		# Lissage de la courbe
		intrafic = sg_filter.smooth([speed[0] for speed in self.speed],self.coeff)
		outtrafic = sg_filter.smooth([speed[1] for speed in self.speed],self.coeff)
		
		plt.plot(times, intrafic,"k-",
			times, outtrafic,"b-")
		plt.fill_between(times,intrafic,0,color='g')
		
		# Calcul des axes
		debitmax = max([max(intrafic),max(outtrafic)])
		plt.axis([config.TIME,0,0,debitmax + debitmax/10])
		
		if not decoration:
			plt.axis('off')
		else :
			plt.xlabel("Temps ecoule(en minutes)")
			plt.ylabel("Debit (en ko/s)")
		plt.savefig(file_,dpi=width/8)

for plugin in config.PLUGINS :
	mg = MonitorGraph(plugin)
	mg.getData()
	mg.positionToSpeed()
	mg.gen_picture(config.IMAGES_PATH + '/' + plugin, width = 800, decoration = True)
	mg.gen_picture(config.IMAGES_PATH + '/mini_' + plugin, width = 200, decoration = False)
