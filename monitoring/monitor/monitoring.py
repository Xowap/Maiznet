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
import monitor


class Monitoring(object):
	def __init__(self):
		self.mp = monitor.MonitorProtocol()
	
	def xDSL(self,line):
		
                try :
		        value = self.mp.fetchValue(config.PRE_PING_PLUGINS_MUNIN+str(line))[0]
		        if value != "100.0":
			        return "OK"
		        return "KO"
                except :
                        return "KO"
	
	def jabber(self):
		try :
			from jabber import jabber
			connex = jabber.Client(host=config.JABBER_SERVER,debug=[], port=config.JABBER_PORT)
			connex.connect()
			return "OK"
		except :
			return "KO"

m = Monitoring()
services = {}
for key in config.SERVICES:
	method = getattr(m,config.SERVICES[key][0])
	if config.SERVICES[key][1]:
		services[key] = method(config.SERVICES[key][1])
	else :
		services[key] = method()
wfile = open(config.STATE_PATH,"w")
wfile.write(json.dumps(services))
wfile.close()
