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

import commands
import json
import config

class Monitoring(object):
	def __init__(self):
		pass
	
	def xDSL(self,line):
		c = commands.getoutput('ping -c 1 -S ' + config.IP_xDSL[line-1] + ' google.fr | grep "0%"')
		state = c.split()
		if state[5] == "0%"!
			return "OK"
		return "KO"
	
	def jabber(self):
		c = commands.getoutput("check_jabber -H " + config.JABBER_SERVER + " -p " + config.JABBER_PORT)
		state = c.split()
		if state[1] == 'OK':
			return "OK"
		return "KO"

m = Monitoring()
services = {"ADSL1":m.xDSL(1),"ADSL2":m.xDSL(2),"SDSL":m.xDSL(3),"jabber":m.jabber()}
wfile = open(config.STATE_PATH,"w")
wfile.write(json.dumps(services))
