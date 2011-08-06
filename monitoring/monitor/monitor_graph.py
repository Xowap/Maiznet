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
		self.speed = False
		self.real_data = []
	
	def getData(self):
		"""
		Récupère les données de la base de données
		"""
		self.cursor.execute("SELECT * FROM %s ORDER BY date DESC" % self.plugin[0]) 
		self.data = self.cursor.fetchall()[1:]
	
	def positionToSpeed(self):
		"""
		Calcule une liste de vitesse depuis une liste de positions
		"""
		self.real_data = []
		self.speed = True

		for data in self.data:
			if self.data.index(data) == 0:
				continue
			d = self.data[self.data.index(data)-1]
			if d[1] < data[1] or d[2] < data[2]:
				continue
			date1 = parseDateTime(str(d[3]))
			date2 = parseDateTime(str(data[3]))
			times = (date1-date2).seconds
			
			self.real_data.append([
				(d[1] - data[1])/times,
				(d[2] - data[2])/times,
				(datetime.datetime.now()-date1).seconds/60
				
			])
	
	def process_data(self):
		p = False
		if not self.real_data:
			p = True
			self.real_data.extend(self.data)
		self.real_data = zip(*self.real_data)
		self.real_data = [ list(data) for data in self.real_data]

		if not self.speed :
			self.real_data = self.real_data[1:]
			self.real_data[2] = [(datetime.datetime.now() - parseDateTime(str(date))).seconds/60 for date in self.real_data[-1]]

	def gen_picture(self,file_,width,decoration):
		"""
		Génère une image
		"""
		self.process_data()
		# Lissage de la courbe
		self.real_data[0] = sg_filter.smooth(self.real_data[0],self.coeff)
		self.real_data[1] = sg_filter.smooth(self.real_data[1],self.coeff)

		plt.clf()
		plt.cla()
		
		plt.plot(self.real_data[-1], self.real_data[0],"k-",
			self.real_data[-1], self.real_data[1],"b-")
		plt.fill_between(self.real_data[-1],self.real_data[0],0,color='g')
		

		# Calcul des axes
		debitmax = max([max(self.real_data[0]),max(self.real_data[1])])
		plt.axis([config.TIME,1,0,debitmax + debitmax/10])
		
		if not decoration:
			plt.axis('off')
		else :
			plt.xlabel("Temps ecoule(en minutes)")
			plt.ylabel(self.plugin[1])
		plt.savefig(file_,dpi=width/8)

for plugin in config.PLUGINS :
	mg = MonitorGraph(plugin)
	mg.getData()
	if "if_" in plugin[0] :
		mg.positionToSpeed()
	mg.gen_picture(file_ = "%s/%s.png" % (config.IMAGES_PATH,plugin[0]), width = 800, decoration = True)
	#mg.gen_picture(file_ = config.IMAGES_PATH + '/mini_' + plugin + ".png", width = 200, decoration = False)
