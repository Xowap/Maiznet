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

PORT_MUNIN=4949
IP_MUNIN="192.168.0.1"
PRE_PING_PLUGINS_MUNIN="ping_re"
IMAGES_PATH = relpath + "/../../media/monitoring/"
JABBER_SERVER = "192.168.0.16"
JABBER_PORT=5222
STATE_PATH = relpath + "/state"
SERVICES = {"ADSL1":["xDSL",1],"ADSL2":["xDSL",2],"ADSL3":["xDSL",3],"SDSL":["xDSL",4],"Jabber":["jabber",None]}
SMOKEPING = "/var/cache/smokeping/images/Lignes/"
