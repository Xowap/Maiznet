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
		if state[5] == "0%":
			return "OK"
		return "KO"
	
	def jabber(self):
		c = commands.getoutput("/usr/lib/nagios/plugins/check_tcp -H " + config.JABBER_SERVER + " -p " + str(config.JABBER_PORT) + """ -s "<stream:stream to='host' xmlns='jabber:client' xmlns:stream='http://etherx.jabber.org/streams'>" -e "<?xml version='1.0' encoding='UTF-8'?><stream:stream xmlns:stream=\\"http://etherx.jabber.org/streams" xmlns="jabber:client\\"" -w 3 -c 5 -v """)
		state = c.split()
		if state[1] == 'OK':
			return "OK"
		return "KO"

m = Monitoring()
print m.jabber()
#services = {"ADSL1":m.xDSL(1),"ADSL2":m.xDSL(2),"SDSL":m.xDSL(3),"jabber":m.jabber()}
#wfile = open(config.STATE_PATH,"w")
#wfile.write(json.dumps(services))
