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

import os

relpath = os.path.dirname(os.path.realpath(__file__))

DATABASE = relpath + "/monitor.db" 
TIME=120
PORT_MUNIN=4949
IP_MUNIN="192.168.0.1"
PLUGINS = ["if_re1","if_re2","if_re3"]
IMAGES_PATH = relpath+"/../../media/monitoring/"
LISSAGE_NUM_POINTS = 10
LISSAGE_COEFF = 10
JABBER_SERVER = "192.168.0.10"
JABBER_PORT=5222
IP_xDSL = ["192.168.1.10","192.168.2.10","192.168.3.10"]
STATE_PATH = relpath + "/state"
