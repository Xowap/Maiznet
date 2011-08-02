#-*- coding:utf-8 -*-
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
	def __init__(self,plugin,basepath="/root/monitor/monitor.db"):
		self.connection = sqlite.connect(basepath)
		self.cursor = self.connection.cursor()
		self.plugin = plugin
		self.now = datetime.datetime.now()
		self.coeff = sg_filter.calc_coeff(30,19)
	
	def getData(self):
		"""
		Récupère les données de la base de données
		"""
		self.cursor.execute("SELECT * FROM " + self.plugin + " ORDER BY date DESC") 
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
	
	def miniature(self,width):
		plt.savefig("mini_"+self.plugin+".png",dpi=width/8)

	def traceSpeed(self,minutes):
		"""
			Trace le graphe.
		"""
		times = [speed[2] for speed in self.speed]
		intrafic = sg_filter.smooth([speed[0] for speed in self.speed],self.coeff)
		outtrafic = sg_filter.smooth([speed[1] for speed in self.speed],self.coeff)
		plt.plot(times, intrafic,"k-",
			times, outtrafic,"b-")
		plt.fill_between(times,intrafic,0,color='g')
		debitmax = max([max(intrafic),max(outtrafic)])
		plt.axis([minutes,0,0,debitmax + debitmax/10])
		
		self.miniature(200)

		plt.xlabel("Temps ecoule(en minutes)")
		plt.ylabel("Debit (en ko/s)")
		plt.savefig("re1.png")

mg = MonitorGraph("if_re1")
mg.getData()
mg.positionToSpeed()
mg.traceSpeed(120)
