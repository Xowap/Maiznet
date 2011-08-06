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
from sqlite3 import dbapi2 as sqlite


class Monitoring(object):
	def __init__(self):
		self.connection = sqlite.connect(config.DATABASE)
		self.cursor = self.connection.cursor()
	
	def xDSL(self,line):
		value = self.cursor.execute('SELECT `packetloss` FROM ping_re%s ORDER BY date DESC' % str(line)).fetchone()
		if value != 0:
			return "OK"
		return "KO"
	
	def jabber(self):
		c = commands.getoutput("/usr/lib/nagios/plugins/check_tcp -H " + config.JABBER_SERVER + " -p " + str(config.JABBER_PORT) + """ -s "<stream:stream to='host' xmlns='jabber:client' xmlns:stream='http://etherx.jabber.org/streams'>" -e "<?xml version='1.0' encoding='UTF-8'?><stream:stream xmlns:stream=\\"http://etherx.jabber.org/streams" xmlns="jabber:client\\"" -w 3 -c 5 -v """)
		state = c.split()
		if state[1] == 'OK':
			return "OK"
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
