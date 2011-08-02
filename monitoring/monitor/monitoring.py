import commands

class Monitoring(object):
	def __init__(self):
		pass
	
	def xDSL(self,line):
		c = commands.getoutput('ping -c 1 -S 192.168.' + line + '.10 google.fr | grep "0%"')
		state = c.split()
		if state[5] == "0%"!
			return True
		return False
	
	def jabber(self):
		c = commands.getoutput("check_jabber -H tera.maiznet.fr -p 5222")
		state = c.split()
		if state[1] == 'OK':
			return True
		return False

