import commands
import json
import os

relpath = os.path.dirname(os.path.realpath(__file__))

class Monitoring(object):
	def __init__(self):
		pass
	
	def xDSL(self,line):
		c = commands.getoutput('ping -c 1 -S 192.168.' + line + '.10 google.fr | grep "0%"')
		state = c.split()
		if state[5] == "0%"!
			return "OK"
		return "KO"
	
	def jabber(self):
		c = commands.getoutput("check_jabber -H tera.maiznet.fr -p 5222")
		state = c.split()
		if state[1] == 'OK':
			return "OK"
		return "KO"

m = Monitoring()
services = {"ADSL1":m.xDSL(1),"ADSL2":m.xDSL(2),"SDSL":m.xDSL(3),"jabber":m.jabber()}
wfile = open(relpath+"/state","w")
wfile.write(json.dumps(services))
